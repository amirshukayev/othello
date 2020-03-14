"""
negamax alpha beta Othello player
"""

from oth_board import EMPTY, BLACK, WHITE
from time import time

WIN = 'win'
LOSS = 'lose'
DRAW = 'draw'
ABORTED = 'aborted'

INF = 1e9

class OthelloPlayerAB:

    def __init__(self, board):
        """
        creates solver for the current board
        """
        self.super_debug = False

        self.board = board
        self.time_limit = 60 # 1 minute time limit by default
        self.start = -INF

        self.searches = 0
        self.terminals = 0

    def SetTimeLimit(self, time_limit):
        """
        set time limit of the search in seconds
        """
        self.time_limit = time_limit

    def GetStats(self):
        return {
            'searches': self.searches,
            'searches_per_second': round(self.searches / self.time_limit, 4),
            'terminals': self.terminals
        }

    def Solve(self):
        """
        solves board's current position for the current player
        returns following:
        result, time_taken
        """
        self.start = time()
        self.searches = 0
        self.terminals = 0

        result = self._ab()

        if self.Abort():
            return ABORTED, -1

        return result, time() - self.start

    def Abort(self):
        """
        return true if we should abort currently running search
        """
        if time() - self.start > self.time_limit:
            return True
        return False

    def TTread(self):
        """
        read result from the transposition table
        """
        pass

    def TTwrite(self, result):
        """
        write result to the transpotition table
        """
        pass

    def _ab(self):
        """
        return if current move is win, loss, or some abritrary score (float)
        IMPORTANT: GAME IS NOT OVER IS NO LEGAL MOVES, USE OthBoard.Terminal()
        """
        self.searches += 1

        if len(self.board.move_history) > self.board.size ** 2 - 4:
            raise RuntimeError("move history too long")

        if self.Abort():
            return LOSS

        if self.board.Terminal():

            self.terminals += 1
            winner, _ = self.board.Winner()

            if winner == EMPTY:
                raise RuntimeError("can't handle DRAWS yet")
                return DRAW

            if self.board.CurrentPlayer() == winner:
                return WIN

            return LOSS

        if self.super_debug:
            print(self.board)

        moves = self.board.GetLegalMoves()

        for m in moves:

            if not self.board.Play(m):
                raise RuntimeError("illegal move played")

            result = Nega(self._ab())

            self.board.Undo()

            if result == WIN:
                if self.super_debug:
                    print("beta cut")
                return WIN

        return LOSS
            

def Nega(result):
    """
    do the Nega part of negamax alpha beta
    """
    if result == WIN:
        return LOSS
    elif result == LOSS:
        return WIN
    else:
        return result