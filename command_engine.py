"""
parses commands and executes them on a given board
"""

import sys

SUCCEED = 1

class CommandEngine:

    def __init__(self, board):
        """
        constructor, board should be an OthBoard
        """
        self.board = board
        self.commands = {
            "commands": self._commands_cmd,
            "moves": self._legal_moves_cmd,
            "play": self._play_cmd,
            "showboard": self._show_board_cmd,
            "undo": self._undo_cmd
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
            cmd, args = line[0], line[1:]
            self.commands[cmd](args)


    def _commands_cmd(self, args):
        print(' '.join(self.commands.keys()))


    def _legal_moves_cmd(self, args):
        print(' '.join(self.board.GetLegalMoves()))


    def _play_cmd(self, args):
        if not self.board.Play(args[0]):
            return "Illegal Move"

    def _show_board_cmd(self, args):
        print(self.board)

    def _undo_cmd(self, args):
        self.board.Undo()
