/*
Board representation for the game Othello
includes logic for legal moves, and ability to undo moves
(includes move history)
*/

#ifndef OTH_BOARD_H
#define OTH_BOARD_H

#include <assert.h>
#include <string>
#include <vector>

#define dp__ printf("LINE #%d FILE: %s\n", _LINE_, _FILE_);

typedef int othColor;
typedef std::pair<int,int> othPoint;
typedef std::vector<othPoint> othPointList;
typedef std::vector<othColor> othColorList;
typedef std::vector<std::pair<othPoint,othPointList> > othHistory;

#define EMPTY 0
#define BLACK 1
#define WHITE 2
#define BORDER 3

#define INF 200002

inline othColor opp(othColor color) 
{
    if (color == BLACK)
        return WHITE;

    else if (color == WHITE)
        return BLACK;

    assert(false);
}

inline othPoint p(int x, int  y) 
{
    return std::make_pair(x, y);
}

inline bool is_pass(othPoint pt)
{
    return (pt.first == INF) &&
        (pt.second == INF);
}

class OthBoard
{
public:
    OthBoard(int size);
    ~OthBoard();
    
    void ChangeSize(int size);
    void Reset();
    std::string Str();
    int Size();

    uint64_t Hash() const;
    std::string PointToString(othPoint move) const;
    othPoint StrToPoint(std::string str) const;

    othColor CurrentPlayer() const;
    std::string CurrentPlayerStr() const;
    othPointList AllPointsBeside(othPoint move) const;

    othColor AccessBoard(othPoint pt) const;
    void SetBoard(othPoint pt, othColor);

    othPointList GetCaptures(othPoint p) const;
    bool IsLegal(othPoint p) const;

    // return true if legal
    bool Play(othPoint p);
    void Undo();
    bool Terminal();
    std::pair<othColor,float> Winner() const;

    void Place(othPoint p, othColor c);
    othPointList GetLegalMoves();
    othHistory GetHistory();

    int PointToIndex(othPoint pt);

private:
    bool InBounds(othPoint p) const;
    void InitDirs();

// members
private:
    int m_size;
    bool m_allowOddSizedBoards;
    float m_komi;

    othColorList m_board;
    othHistory m_history;
    othColor m_currentPlayer;

    othPointList m_dirs;
};

inline int OthBoard::Size()
{
    return m_size;
}

#endif
