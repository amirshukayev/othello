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
        self.super_debug = True

        self.board = board
        self.time_limit = 60 # 1 minute time limit by default
        self.start = -INF

        self.searches = 0
        self.terminals = 0

    def GetStats(self):
        return {
            'searches': self.searches,
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
            return ABORTED

        return result, time() - self.start

    def Abort(self):
        """
        return true if we should abort currently running search
        """
        if time() - self.start > self.time_limit:
            return True
        return False

    def _ab(self):
        """
        return if current move is win, loss, or some abritrary score (float)
        IMPORTANT: GAME IS NOT OVER IS NO LEGAL MOVES, USE OthBoard.Terminal()
        """
        self.searches += 1

        if self.super_debug:
            print(self.board)
            print()

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

        moves = self.board.GetLegalMoves()

        for m in moves:

            self.board.Play(m)
            result = Nega(self._ab())

            self.board.Undo()

            if result == WIN:
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