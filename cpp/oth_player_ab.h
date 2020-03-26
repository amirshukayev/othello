/*
negamax alpha beta Othello player
*/

#ifndef OTH_PLAYER_AB_H
#define OTH_PLAYER_AB_H

#include "oth_board.h"

#include <algorithm>
#include <string>
#include <map>
#include <chrono>

typedef std::map<std::string,double> AbStats;
typedef std::pair<othColor,double> AbSolveResults;

typedef int AbResult;
typedef std::map<othPoint,double> AbOrderingMap;

#define AB_WIN 0
#define AB_LOSS 1
#define AB_DRAW 2
#define AB_ABORTED 3

#define inf 1e9

// AbResult Nega(AbResult r)
// {
//     if (r == WIN)
//         return LOSS;
//     else if (r == LOSS)
//         return WIN;
//     return r;
// }

class OthelloPlayerAb
{
public:
    OthelloPlayerAb(OthBoard* board);
    ~OthelloPlayerAb();

    void SetTimeLimit(double tl);
    AbStats GetStats();

    AbSolveResults Solve();
    OthBoard Board();

private:
    void CreateMoveOrdering();
    void CreateKiller();
    void UpdateKiller(othPoint m);
    void OrderMoves(othPointList& moves);
    void OrderKiller(othPointList& moves);
    bool Abort();

    AbResult AB();
    AbResult Nega(AbResult r);


private:
    OthBoard* m_board;
    bool m_superDebug;
    double m_timeLimit;
    double m_start;
    double m_timeTaken;
    
    // search statistics
    int m_searches;
    int m_terminals;
    bool m_useTT;
    int m_betaCuts;

    bool m_useOrdering;
    AbOrderingMap m_ordering;

    bool m_useKiller;
    AbOrderingMap m_killer;
};

#endif // OTH_PLAYER_AB_H
