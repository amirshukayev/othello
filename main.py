
from oth_board import OthBoard
from command_engine import CommandEngine
from oth_player_ab import OthelloPlayerAB

if "__main__" == __name__:
    board = OthBoard(4)
    solver = OthelloPlayerAB(board)

    cmd_engine = CommandEngine(board, solver)
    cmd_engine.run()
