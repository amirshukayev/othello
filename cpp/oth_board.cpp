/*
Board representation for the game Othello
includes logic for legal moves, and ability to undo moves
(includes move history)
*/

#include "oth_board.h"

#include <iostream>
#include <sstream>

OthBoard::OthBoard(int size)
{   
    // make sure its not too big
    assert(size > 0 && size < 10);

    m_allowOddSizedBoards = true;
    m_size = size;
    m_komi = 0.5f;
    Reset();
    InitDirs();
}

OthBoard::~OthBoard()
{ }

void OthBoard::InitDirs()
{
    m_dirs.push_back(p(-1, -1));
    m_dirs.push_back(p(-1, 0));
    m_dirs.push_back(p(-1, 1));
    m_dirs.push_back(p(0, -1));

    m_dirs.push_back(p(0, 1));
    m_dirs.push_back(p(1, -1));
    m_dirs.push_back(p(1, 0));
    m_dirs.push_back(p(1, 1));

    m_dirs.push_back(p(0, 0));
}

void OthBoard::Reset()
{
    int n = m_size * m_size;
    m_board = othColorList(n, EMPTY);
    m_history = othHistory();
    m_currentPlayer = BLACK;

    int m2 = m_size / 2;
    int m1 = m2 - 1;

    Place(p(m1, m1), WHITE);
    Place(p(m2, m2), WHITE);
    Place(p(m1, m2), BLACK);
    Place(p(m2, m1), BLACK);
}

std::string ColorToString(othColor c)
{
    if (c == WHITE)
        return std::string("O");
    
    else if (c == BLACK)
        return std::string("X");
    
    else if (c == EMPTY)
        return std::string(" ");

    return std::string();
}

std::string OthBoard::Str()
{
    std::stringstream ss;
    ss << " ";
    for (int i = 0; i < m_size; i++)
    {
        ss << " " << ((char) (i + 'A'));
    }
    ss << std::endl;

    for (int i = 0; i < m_size; i++)
    {
        ss << i+1;
        for (int j = 0; j < m_size; j++)
        {
            ss << " " << ColorToString(AccessBoard(p(j, i)));
        }
        ss << std::endl;
    }
    ss << "to play: " << ColorToString(CurrentPlayer());
    return ss.str();
}

std::string OthBoard::PointToString(othPoint point) const
{
    return std::string{(char)(point.first + 'A'), (char)(point.second + '1')};
}

othPoint OthBoard::StrToPoint(std::string str) const
{
    int x = str[0] - 'A';
    int y = str[1] - '1';
    return p(x, y);
}

void OthBoard::ChangeSize(int size)
{
    m_size = size;
    Reset();
}

othColor OthBoard::CurrentPlayer() const
{
    return m_currentPlayer;
}

std::string OthBoard::CurrentPlayerStr() const
{
    if (m_currentPlayer == BLACK)
        return std::string("black");
    
    if (m_currentPlayer == WHITE)
        return std::string("white");
    
    // current player must be BLACK or WHITE
    assert(false);
}

bool OthBoard::InBounds(othPoint point) const
{
    return (point.first >= 0 && point.first < m_size)
        && (point.second >= 0 && point.second < m_size);
}

othPointList OthBoard::AllPointsBeside(othPoint point) const
{
    int x = point.first, y = point.second;
    othPointList ret;
    for (auto const& dp : m_dirs)
    {
        int dx = dp.first, dy = dp.second;
        othPoint pt = p(x+dx, y+dy);

        if (InBounds(pt))
        {
            ret.push_back(pt);
        }
    }
    return ret;
}

othColor OthBoard::AccessBoard(othPoint pt) const
{
    int sz = m_size;
    int idx = sz * pt.first + pt.second;
    return m_board[idx];
}

void OthBoard::SetBoard(othPoint pt, othColor c)
{
    int sz = m_size;
    int idx = sz * pt.first + pt.second;
    m_board[idx] = c;
}

othPointList OthBoard::GetCaptures(othPoint pt) const
{
    othColor our_color = CurrentPlayer();
    int x = pt.first, y = pt.second;

    if (!InBounds(pt))
    {
        return othPointList();
    }

    if (AccessBoard(pt) != EMPTY)
    {
        return othPointList();
    }

    othPointList all_captures = othPointList();

    bool legal_flag = false;
    // check in all 8 directions (othello works diagonally too)
    for (auto const& dpt : m_dirs)
    {
        int dx = dpt.first, dy = dpt.second;
        int cx = x+dx, cy = y+dy;

        bool seen_opp = false;
        othPointList tmp_captures = othPointList();

        othPoint cpt = p(cx, cy);
        while (InBounds(cpt))
        {
            if (AccessBoard(cpt) == opp(our_color))
            {
                tmp_captures.push_back(cpt);
                seen_opp = true;
            }

            else if (AccessBoard(cpt) == EMPTY)
            {
                tmp_captures.clear();
                break;
            }

            else if (AccessBoard(cpt) == our_color && seen_opp)
            {
                all_captures.insert(all_captures.end(), 
                                    tmp_captures.begin(), 
                                    tmp_captures.end());
                tmp_captures.clear();
                break;
            }

            cx += dx;
            cy += dy;
            cpt = p(cx, cy);
        }
    }
    return all_captures;
}

bool OthBoard::IsLegal(othPoint pt) const
{
    if (!GetCaptures(pt).empty())
    {
        return true;
    }
    return false;
}

bool OthBoard::Play(othPoint pt)
{
    if (is_pass(pt)) {
        // shouldn't be able to pass during AB search
        assert(false);
        m_currentPlayer = opp(m_currentPlayer);
    }

    auto captures = GetCaptures(pt);
    if (captures.empty())
        return false;

    SetBoard(pt, CurrentPlayer());
    for (auto const& cpt : captures)
        SetBoard(p(cpt.first, cpt.second), CurrentPlayer());

    m_currentPlayer = opp(CurrentPlayer());
    // todo: maybe push pointers with new here, to avoid copies
    m_history.push_back(make_pair(pt, captures));

    return true;
}

void OthBoard::Undo()
{
    othPoint pt = m_history.back().first;
    othPointList captures = m_history.back().second;
    m_history.pop_back();

    SetBoard(pt, EMPTY);
    for (auto const& cpt : captures)
        SetBoard(cpt, CurrentPlayer());

    m_currentPlayer = opp(m_currentPlayer);
}

bool OthBoard::Terminal()
{
    if (GetLegalMoves().empty())
        return false;

    m_currentPlayer = opp(m_currentPlayer);
    if (GetLegalMoves().empty())
    {
        m_currentPlayer = opp(m_currentPlayer);
        return false;
    }

    m_currentPlayer = opp(m_currentPlayer);
    return true;
}

std::pair<othColor,float> OthBoard::Winner() const
{
    int bcount = 0, wcount = 0;
    
    for (int i = 0; i < m_size; i++)
    {
        for (int j = 0; j < m_size; j++)
        {
            othColor c = AccessBoard(p(i, j));
            if (c == BLACK)
            {
                bcount++;
            }
            else if (c == WHITE)
            {
                wcount++;
            }
        }
    }

    float score = bcount - wcount + m_komi; // komi to make sure we don't tie for now
    if (score > 0.0)
    {
        return std::make_pair(BLACK, score);
    }
    else if (score < 0.0) 
    {
        return std::make_pair(WHITE, score);
    }
    else 
    {
        // score should not be 0 with komi
        assert(false);
        return std::make_pair(EMPTY, score);
    }
}

uint64_t OthBoard::Hash() const
{
    return 1;
}

void OthBoard::Place(othPoint pt, othColor c)
{
    assert(c == BLACK || c == WHITE || c == EMPTY);
    int x = pt.first, y = pt.second;
    SetBoard(p(x, y), c);
}

othPointList OthBoard::GetLegalMoves()
{
    othPointList moves;
    for (int i = 0; i < m_size; i++)
    {
        for (int j = 0; j < m_size; j++)
        {
            othPoint pt = p(i, j);
            if (IsLegal(pt))
            {
                moves.push_back(pt);
            }
        }
    }
    return moves;
}
