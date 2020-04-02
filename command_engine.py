"""
parses commands and executes them on a given board
"""

import sys
from oth_player_ab import WIN, LOSS, DRAW, ABORTED, MAXIMUM_DEPTH

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
            "play_game": self._play_game_cmd,
            "reset": self._reset_cmd,
            "set_size": self._set_size_cmd,
            "time_limit": self._set_time_limit_cmd,
            "showboard": self._show_board_cmd,
            "best_move": self._best_move,
            "solve": self._solve_cmd,
            "undo": self._undo_cmd,
            "use_killer": self._use_killer_cmd,
            "use_ordering": self._use_ordering_cmd,
            "use_tt": self._use_tt_cmd,
            "self_play": self._self_play
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

    # Returns a best move for colour args from state
    def _best_move(self, args):
        result = self.engine.BestMove()
        print(result[1])
        if result[0]:
            print('Search has hit maximum depth, no win or loss calculated')
        print('Top move: {}'.format(result))

    def _self_play(self, args):
        while True:
            # Get a move:
            move = self.engine.BestMove()

            # If there are no legal moves
            if not move[1]:
                winner, score = self.board.Winner()
                print("Winner is {}, with score {}".format(winner, score))
                return False

            # Play Move:
            if not self.board.Play(move[1]):
                print("Illegal Move")

            # Set to other player:
            print(self.board)
            if self.board.Terminal():
                winner, score = self.board.Winner()
                print("Winner is {}, with score {}" .format(winner, score))
                return False
            print("")

    def _legal_moves_cmd(self, args):
        legal_moves = self.board.GetLegalMoves()
        if not legal_moves:
            print('pass')
        else:
            print(' '.join(legal_moves))

    def _play_cmd(self, args):
        if not self.board.Play(args[0]):
            print("Illegal Move")

    def _play_game_cmd(self, args):
        # Get the first or second player:
        if int(args[0]) == 1:
            while True:
                print(self.board)

                if self.board.Terminal():
                    winner, score = self.board.Winner()
                    print("Winner is {}, with score {}".format(winner, score))
                    return False

                while True:

                    if len(self.board.GetLegalMoves()) == 0:
                        print("No legal moves")
                    else:
                        print("Legal Moves: {}" .format(self.board.GetLegalMoves()))
                        player_move = input("What is your move? ")
                        # Play Move:
                        if not self.board.Play(player_move):
                            print("Illegal Move")
                        else:
                            break

                move = self.engine.BestMove()

                if not move[1]:
                    winner, score = self.board.Winner()
                    print("Winner is {}, with score {}".format(winner, score))
                    return False

                # Play Move:
                if not self.board.Play(move[1]):
                    print("Illegal Move")

                print("")

        # player goes second.
        elif int(args[0]) == 2:
            while True:
                move = self.engine.BestMove()

                if not move[1]:
                    winner, score = self.board.Winner()
                    print("Winner is {}, with score {}".format(winner, score))
                    return False

                # Play Move:
                if not self.board.Play(move[1]):
                    print("Illegal Move")

                print(self.board)

                while True:
                    if len(self.board.GetLegalMoves()) != 0:
                        print("Legal Moves: {}".format(self.board.GetLegalMoves()))
                        player_move = input("What is your move? ")
                        # Play Move:
                        if not self.board.Play(player_move):
                            print("Illegal Move")
                        else:
                            break
                    else:
                        print("No Legal Moves")

                if self.board.Terminal():
                    winner, score = self.board.Winner()
                    print("Winner is {}, with score {}".format(winner, score))
                    return False
                print("")

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
        result, _time, score = self.engine.Solve()
        if result == WIN:
            print('{} wins. Search took {}s'.format(self.board.CurrentPlayerStr(), _time))
        elif result == LOSS:
            print('{} loses. Search took {}s'.format(self.board.CurrentPlayerStr(), _time))
        elif result == ABORTED:
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
