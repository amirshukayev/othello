"""
Board representation for the game Othello
includes logic for legal moves, and ability to undo moves
(includes move history)
"""

EMPTY = 0
BLACK = 1
WHITE = 2
BORDER = 3

DIRS = [(-1, -1), (-1, 0), (-1, 1), 
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)]

LETTERS = [chr(x) for x in range(ord('A'), ord('Z')+1)]

SYMBOLS = {
    EMPTY: '.',
    BLACK: 'X',
    WHITE: 'O'}

def opp(color):
    """
    returns opponent of given color
    """
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK
    else:
        assert(FALSE)

class OthBoard:

    def __init__(self, size):
        """
        create Othello Board of size <size * size>
        max size of 10 for now
        """
        assert(size > 0 and size < 10)
        assert(not size % 2)

        self.size = size
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        self.move_history = []
        self.current_player = BLACK


    def __str__(self):
        """
          A B C D
        1 . . . . 
        2 . X O . 
        3 . O X .
        4 . . . .
        to play: {BLACK, WHITE}
        """
        lines = ['  ' + ' '.join(LETTERS[0:self.size])]

        for i, row in enumerate(self.board):
            line = [str(i)]
            line += [SYMBOLS[x] for x in row]
            lines.append(' '.join(line))

        lines.append("to play: {}".format(SYMBOLS[self.current_player]))
        return '\n'.join(lines)


    def CurrentPlayer(self):
        """
        player who moves next
        """
        return self.current_player

    def IsLegal(self, move):
        """
        tells us if move is legal
        """
        pass

    def Play(self, move):
        """
        play at point move 
        """
        pass

