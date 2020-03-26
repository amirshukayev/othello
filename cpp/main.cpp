/*
create board, engine, and solver
*/

#include "oth_board.h"
#include "command_engine.h"
#include "oth_player_ab.h"

int main()
{
    OthBoard* board = new OthBoard(4);
    OthelloPlayerAb abPlayer(board);
    CommandEngine cmdEngine(board, abPlayer);
    cmdEngine.Run();
    delete board;
}
