"""
negamax alpha beta Othello player
"""

from oth_board import EMPTY, BLACK, WHITE
from time import time
from random import randint
from collections import defaultdict

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

        # transposition table
        self.use_tt = False
        self.tt_size = -1
        self.tt = {}
        self.tt_size = 100000 # make it this big for now

        # move ordering
        self.use_ordering = True
        self._ordering = {}

        # killer heuristic
        self.use_killer = True
        self._killer = {}

    def SetTimeLimit(self, time_limit):
        """
        set time limit of the search in seconds
        """
        self.time_limit = time_limit

    def GetStats(self):
        return {
            'searches': self.searches,
            'searches_per_second': round(self.searches / self.time_taken, 4),
            'terminals': self.terminals,
            'beta_cuts': self.beta_cuts,
            'tt_hits': self.tt_hits,
            'tt_misses': self.tt_misses,
            'tt_gcs': self.tt_gcs
        }

    def CreateMoveOrdering(self):
        """
        creates dictionary of move -> weight
        lower weights are better, and moves with lower weights will be picked first
        """
        self._ordering = defaultdict(float)

        # corners first
        limit = self.board.size - 1
        corners = [(0, 0), (0, limit), (limit, 0), (limit, limit)]
        for c in corners:
            self._ordering[c] = -10
            # so the ordering doesn't care about the format of the move (messy)
            self._ordering[self.board.PointToStr(c)] = -10

        # points beside the corners are also weak
        for c in corners:
            for p in self.board.AllPointsBeside(c):
                self._ordering[p] = 10
                # so the ordering doesn't care about the format of the move (messy)
                self._ordering[self.board.PointToStr(p)] = 10

    def CreateKiller(self):
        """
        maps moves to number of beta cuts it did
        """
        self._killer = {}

        # basically corners will already be assumed
        # to have created a bunch of beta cuts
        # so they are prefered (if move ordering on too)
        ordering_init_multiplier = (self.board.size ** 2) // 2

        if self.use_ordering:
            if not self._ordering:
                self.CreateMoveOrdering()
            for key in self._ordering:
                self._killer[key] = ordering_init_multiplier * self._ordering[key]
            

    def UpdateKiller(self, m):
        """
        incrememnts number of beta cuts for a move
        """
        if m not in self._killer:
            self._killer[m] = 0
        self._killer[m] += 1

    def OrderMoves(self, moves):
        """
        orders moves based on the move ordering, lower is stronger and will
        be picked first
        """
        return sorted(moves, key=lambda x: self._ordering.get(x, 0.0))

    def OrderKiller(self, moves):
        """
        orders moves based on the killer heuristic (better moves cause more beta cuts)
        """
        return sorted(moves, key=lambda x: self._killer.get(x, 0))

    def Solve(self):
        """
        solves board's current position for the current player
        returns following:
        result, time_taken
        """
        self.start = time()
        self.beta_cuts = 0
        self.searches = 0
        self.terminals = 0
        self.tt_hits = 0
        self.tt_misses = 0
        self.tt_gcs = 0
        self.time_taken = 0

        # if the size of the current board search is different than
        # previous, we need to reset the transpotition table
        # we can also take this chance to reset the ordering table
        if self.tt_size != self.board.size:
            self.tt = {}
            self.tt_size = self.board.size
            self.CreateMoveOrdering()
            self.CreateKiller()

        if self.use_killer and self.use_ordering:
            print("warning: if both use_killer and use_ordering are set, killer heuristic will not be used")

        result = self._ab()

        self.time_taken = time() - self.start

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
        if not self.use_tt:
            return None

        _key = self.board.Hash()

        # tt hit
        if _key in self.tt:
            self.tt_hits += 1
            return self.tt[_key]

        # tt miss
        else:
            self.tt_misses += 1
            return None

    def TTwrite(self, result):
        """
        write result to the transpotition table
        """
        if not self.use_tt:
            return

        _key = self.board.Hash()
        self.tt[_key] = result

        # garbage collection, make sure tt doesnt get too big and hit swap
        to_remove = []
        if len(self.tt) > self.tt_size:
            self.tt_gcs += 1
            # use sampling to remove 0.25N items from the tt
            for _key in self.tt.keys():
                if randint(0, 3) == 0:
                    to_remove.append(_key)

        # clean up all the chosen enteries
        for _key in to_remove:
            del self.tt[_key]

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

        tt_res = self.TTread()
        if tt_res is not None:
            return tt_res

        if self.board.Terminal():

            self.terminals += 1
            winner, _ = self.board.Winner()

            if winner == EMPTY:
                raise RuntimeError("can't handle DRAWS yet")
                self.TTwrite(DRAW)
                return DRAW

            if self.board.CurrentPlayer() == winner:
                self.TTwrite(WIN)
                return WIN

            self.TTwrite(LOSS)
            return LOSS

        if self.super_debug:
            print(self.board)

        moves = self.board.GetLegalMoves()

        if self.use_ordering and not self.use_killer:
            moves = self.OrderMoves(moves)

        elif self.use_killer:
            moves = self.OrderKiller(moves)

        for m in moves:

            if not self.board.Play(m):
                raise RuntimeError("illegal move played")

            result = Nega(self._ab())

            self.board.Undo()

            if result == WIN:
                self.beta_cuts += 1
                if self.super_debug:
                    print("beta cut")

                if self.use_killer:
                    self.UpdateKiller(m)

                self.TTwrite(WIN)
                return WIN

        self.TTwrite(LOSS)
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