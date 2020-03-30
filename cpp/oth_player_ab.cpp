/*
negamax alpha beta Othello player
*/

#include <iostream>

#include "oth_player_ab.h"

#define TimeCast std::chrono::duration_cast

typedef std::chrono::system_clock Time;
typedef std::chrono::milliseconds Ms;

double Now()
{
    return TimeCast<Ms>(Time::now().time_since_epoch()).count();
}

OthelloPlayerAb::OthelloPlayerAb(OthBoard* board)
    : m_board(board),
      m_useKiller(false),
      m_useOrdering(true),
      m_useTT(false),
      m_superDebug(false),
      m_timeLimit(60.0),
      m_start(-INF),
      m_searches(0),
      m_terminals(0)
{ }

OthelloPlayerAb::~OthelloPlayerAb()
{ 
    std::cout << "destroyed2" << std::endl;
}

void OthelloPlayerAb::SetTimeLimit(double tl)
{
    m_timeLimit = tl;
}

AbStats OthelloPlayerAb::GetStats()
{
    AbStats stats;
    stats["searches"] = m_searches;
    stats["beta cuts"] = m_betaCuts;
    stats["searches_per_second"] = m_searches / m_timeTaken;
    stats["time_taken"] = m_timeTaken;
    stats["terminals"] = m_terminals;
    return stats;
}

void OthelloPlayerAb::CreateMoveOrdering()
{ 
    int limit = m_board->Size() - 1;
    othPointList corners;

    int vecSize = limit * (limit+1);
    m_ordering.resize(vecSize*2, 0.0);
    
    using namespace std;

    corners.push_back(p(0, 0));
    corners.push_back(p(0, limit));
    corners.push_back(p(limit, 0));
    corners.push_back(p(limit, limit));

    for (auto const& pt : corners)
    {
        int idx = m_board->PointToIndex(pt);
        m_ordering[idx] = -10;
    }
    for (auto const& c : corners)
    {
        for (auto const& pt : m_board->AllPointsBeside(c))
        {
            int idx = m_board->PointToIndex(pt);
            m_ordering[idx] = 10;
        }
    }
}

void OthelloPlayerAb::CreateKiller()
{ }

void OthelloPlayerAb::UpdateKiller(othPoint pt)
{ }

void OthelloPlayerAb::OrderMoves(othPointList& moves)
{ 
    std::sort(
        moves.begin(),
        moves.end(),
        [&](const othPoint& left, const othPoint& right) {
            int lidx = m_board->PointToIndex(left);
            int ridx = m_board->PointToIndex(right);
            return m_ordering[lidx] < m_ordering[ridx];
        }
    );
}

void OthelloPlayerAb::OrderKiller(othPointList& moves)
{ }

AbSolveResults OthelloPlayerAb::Solve()
{ 
    m_start = Now();
    m_betaCuts = 0;
    m_searches = 0;
    m_terminals = 0;

    if (m_useOrdering)
    {
        CreateMoveOrdering();
    }
    std::cout << "size of the board: " << m_board->Size() << std::endl;
    
    auto result = AB();
    m_timeTaken = Now() - m_start;

    othColor winningColor = EMPTY;
    if (result == AB_WIN)
        winningColor = m_board->CurrentPlayer();
    else if (result == AB_LOSS)
        winningColor = opp(m_board->CurrentPlayer());

    return std::make_pair(winningColor, m_timeTaken);
}

bool OthelloPlayerAb::Abort()
{ 
    // if (Now() - m_start > m_timeLimit)
    //     return true;
    return false;
}

AbResult OthelloPlayerAb::AB()
{ 
    m_searches++;
    int size = m_board->Size();
    if (m_board->GetHistory().size() > size*size-3)
    {   
        // more than this many moves is illegal
        assert(false);
    }

    if (Abort())
    {
        if (m_superDebug)
            std::cout << "aborted" << std::endl;
        return AB_ABORTED;
    }

    if (m_board->Terminal())
    {
        m_terminals++;
        auto boardResults = m_board->Winner();

        if (boardResults.first == EMPTY)
        {
            // AB shouldn't tie
            assert(false);
            return AB_DRAW;
        }
        if (boardResults.first == m_board->CurrentPlayer())
        {
            return AB_WIN;
        }
        return AB_LOSS;
    }

    if (m_superDebug)
        std::cout << m_board->Str() << std::endl;

    auto moves = m_board->GetLegalMoves();
    if (m_useOrdering)
    {
        OrderMoves(moves);
    }
    else if (m_useKiller)
    {
        OrderKiller(moves);
    }
    for (othPoint pt : moves)
    {
        if (!m_board->Play(pt))
        {
            // illegal move played
            assert(false);
        }
        auto result = Nega(AB());
        m_board->Undo();

        if (result == AB_WIN)
        {
            m_betaCuts++;
            if (m_superDebug)
                std::cout << "beta cut" << std::endl;
            
            if (m_useKiller)
                UpdateKiller(pt);
            return AB_WIN;
        }
    }
    return AB_LOSS;
}

OthBoard OthelloPlayerAb::Board()
{
    return *m_board;
}

AbResult OthelloPlayerAb::Nega(AbResult r)
{
    if (r == AB_WIN)
        return AB_LOSS;
    else if (r == AB_LOSS)
        return AB_WIN;
    return AB_DRAW;
}
