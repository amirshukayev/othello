"""
parses commands and executes them on a given board
"""

import sys
from oth_player_ab import WIN, LOSS, DRAW, ABORTED

SUCCEED = 1

class CommandEngine:

    def __init__(self, board, engine):
        """
        constructor, board should be an OthBoard
        """
        self.board = board
        self.engine = engine

        self.commands = {
            "commands": self._commands_cmd,
            "moves": self._legal_moves_cmd,
            "play": self._play_cmd,
            "reset": self._reset_cmd,
            "set_size": self._set_size_cmd,
            "time_limit": self._set_time_limit_cmd,
            "showboard": self._show_board_cmd,
            "solve": self._solve_cmd,
            "undo": self._undo_cmd,
            "use_killer": self._use_killer_cmd,
            "use_ordering": self._use_ordering_cmd,
            "use_tt": self._use_tt_cmd
        }

    def run(self):
        """
        take input and run commands
        """
        while True:
            print()
            print('=')
            print()
            line = sys.stdin.readline()
            if not line:
                break

            line = line.strip().split()
            if not line:
                continue

            cmd, args = line[0], line[1:]
            self.commands[cmd](args)

    def _commands_cmd(self, args):
        print(' '.join(self.commands.keys()))

    def _legal_moves_cmd(self, args):
        legal_moves = self.board.GetLegalMoves()
        if not legal_moves:
            print('pass')
        else:
            print(' '.join(legal_moves))

    def _play_cmd(self, args):
        if not self.board.Play(args[0]):
            print("Illegal Move")

    def _reset_cmd(self, args):
        self.board.Reset()

    def _set_size_cmd(self, args):
        size = int(args[0])
        self.board.ChangeSize(size)

    def _set_time_limit_cmd(self, args):
        tl = int(args[0])
        self.engine.SetTimeLimit(tl)

    def _show_board_cmd(self, args):
        print(self.board)

    def _solve_cmd(self, args):
        result, _time = self.engine.Solve()
        if result[0] == WIN:
            print('{} wins. Search took {}s'.format(self.board.CurrentPlayerStr(), _time))
            print(result[1])
        elif result[0] == LOSS:
            print('{} loses. Search took {}s'.format(self.board.CurrentPlayerStr(), _time))
            print(result[1])
        elif result[0] == ABORTED:
            print('search aborted after {} seconds'.format(self.engine.time_limit))
        print(self.engine.GetStats())

    def _undo_cmd(self, args):
        self.board.Undo()

    def _use_killer_cmd(self, args):
        if args[0].strip().lower() == "true":
            self.engine.use_killer = True
        elif args[0].strip().lower() == "false":
            self.engine.use_killer = False
        else:
            print('use_killer must be true or false')

    def _use_ordering_cmd(self, args):
        if args[0].strip().lower() == "true":
            self.engine.use_ordering = True
        elif args[0].strip().lower() == "false":
            self.engine.use_ordering = False
        else:
            print('use_ordering must be true or false')

    def _use_tt_cmd(self, args):
        if args[0].strip().lower() == "true":
            self.engine.use_tt = True
        elif args[0].strip().lower() == "false":
            self.engine.use_tt = False
        else:
            print('use_tt must be true or false')
