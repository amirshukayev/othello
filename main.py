
from oth_board import OthBoard
from command_engine import CommandEngine

if "__main__" == __name__:
    engine = CommandEngine(OthBoard(6))
    engine.run()
