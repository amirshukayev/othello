#include "oth_board.h"
#include "command_engine.h"

int main()
{
    OthBoard board(4);
    CommandEngine cmdEngine(board);
    cmdEngine.Run();
}
