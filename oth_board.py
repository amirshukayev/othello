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
        assert(False)

class OthBoard:

    def __init__(self, size):
        """
        create Othello Board of size <size * size>
        max size of 10 for now
        """
        assert(size > 0 and size < 10)
        # you should only be able to set odd size if you choose to
        assert(not size % 2)

        self.allow_odd_size_boards = True
        self.size = size
        self.komi = 0.5 # for simplification purposes for now
        self.Reset()

    def ChangeSize(self, size):
        """
        change size of board, and also reset it
        """
        if size % 2 and not self.allow_odd_size_boards:
            raise ValueError("size of Othello board must be even.")
        
        self.size = size
        self.Reset()

    def Reset(self):
        """
        reset to empty board, beginning of game
        """
        n = self.size ** 2
        self.board = [EMPTY] * n
        self.move_history = []
        self.current_player = BLACK

        m2 = self.size // 2
        m1 = m2 - 1

        self.Place((m1, m1), WHITE)
        self.Place((m2, m2), WHITE)
        self.Place((m1, m2), BLACK)
        self.Place((m2, m1), BLACK)

    def __str__(self):
        """
          A B C D
        1 . . . . 
        2 . X O . 
        3 . O X .
        4 . . . .
        to play: {BLACK, WHITE}
        """
        size = self.size
        tmp_board = [[EMPTY] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                tmp_board[i][j] = self.AccessBoard(i, j)

        lines = ['  ' + ' '.join(LETTERS[0:self.size])]

        # transpose the 2D array so it prints out correctly
        cpboard = [*zip(*tmp_board)]

        for i, row in enumerate(cpboard):
            line = [str(i+1)]
            if self.size > 9 and i < 9:
                line[0] += ' '
            line += [SYMBOLS[x] for x in row]
            lines.append(' '.join(line))

        lines.append("to play: {}".format(SYMBOLS[self.CurrentPlayer()]))
        return '\n'.join(lines)

    def __hash__(self):
        """
        creates hash of the board quickly
        """
        return hash(''.join([SYMBOLS[x] for x in self.board]) + str(self.current_player))

    def PointToStr(self, move):
        """
        for example: (0, 0) -> "A1"
        """
        return LETTERS[move[0]] + str(move[1]+1)

    def StrToPoint(self, _str):
        """
        for example: "A1" -> (0, 0)
        """
        _str = _str.upper()
        return ord(_str[0]) - ord('A'), int(_str[1]) - 1

    def CurrentPlayer(self):
        """
        player who moves next
        """
        return self.current_player

    def CurrentPlayerStr(self):
        """
        string representation of current player (X, O)
        """
        return SYMBOLS[self.current_player]

    def InBounds(self, n):
        """
        if index is within bounds of board (any dimension)
        """
        return 0 <= n < self.size

    def AllPointsBeside(self, p):
        """
        returns array of all points adjacent (including diagonally)
        from point p
        """
        if isinstance(p, str):
            p = self.StrToPoint(p)

        x, y = p
        points = []
        for dx, dy in DIRS:
            if self.InBounds(x+dx) and self.InBounds(y+dy):
                points.append((x+dx, y+dy))
        return points

    def AccessBoard(self, x, y):
        """
        returns the color of the board at point x, y
        """
        sz = self.size
        idc = sz * x + y
        return self.board[idc]

    def SetBoard(self, x, y, color):
        """
        sets the color of the board at point x, y
        """
        sz = self.size
        idc = sz * x + y
        self.board[idc] = color

    def GetCaptures(self, move):
        """
        returns all points captured by this move
        """
        our_color = self.CurrentPlayer()

        x, y = move

        if not self.InBounds(x) or not self.InBounds(y):
            return []

        if self.AccessBoard(x, y) != EMPTY:
            return []

        all_captures = []

        legal = False
        # check in all 8 directions (othello works diagonally)
        for dx, dy in DIRS:
            cx, cy = move
            cx, cy = cx + dx, cy + dy

            seen_opp = False
            tmp_captures = []

            # cx tracks where we are checking
            while self.InBounds(cx) and self.InBounds(cy):

                if self.AccessBoard(cx, cy) == opp(our_color):
                    tmp_captures.append((cx, cy))
                    seen_opp = True

                elif self.AccessBoard(cx, cy) == EMPTY:
                    # illegal line of captures
                    tmp_captures = []
                    break

                elif self.AccessBoard(cx, cy) == our_color and seen_opp:
                    # legal line of capture
                    all_captures += tmp_captures
                    tmp_captures = []
                    break

                cx += dx
                cy += dy

        return all_captures

    def NumCaptured(self, move):
        """
        :param move: the move of a player
        :return: returns an int of the number of pieces captured by a move
        """
        if isinstance(move, str):
            move = self.StrToPoint(move)

        return len(self.GetCaptures(move))

    def EvaluateMove(self, move):
        """
        :param move: The move taken by the agent (needs to be (x, y) tuple form)
        :return: retuns a tuple of two floats based on the desirability of the current state and move
        """
        move = self.StrToPoint(move)

        self.Play(move)
        legal_moves = self.GetLegalMoves()
        player_count = 0
        opponent_count = 0
        move_score = 0.0
        for i in range(self.size):
            for j in range(self.size):
                if self.AccessBoard(i, j) == self.current_player:
                    player_count += 1
                elif self.AccessBoard(i, j) != 0:
                    opponent_count += 1

        # Move Score update on Mobility
        if len(self.move_history) != 0:
            move_score += len(legal_moves) / len(self.move_history)

        self.Undo()

        # Get the difference in the total discs captured.
        captured = self.NumCaptured(move) * len(self.move_history)
        difference = (player_count + captured * 2 + 1 - opponent_count) * len(self.move_history)

        # Start the original action value with the negative number of disc captures
        move_score += float(captured) + difference

        # Check if move creates corner state --> better (checked at all times)
        limit = self.size - 1
        corners = [(0, 0), (0, limit), (limit, 0), (limit, limit)]

        # Check if the current move is a corner play, or if the current state can allow for a corner play
        # Update both values
        for corner in corners:
            if move == corner:
                move_score += -300.0

        return move_score

    # Evaulate the goodness of a state for depth limited AB
    def EvaluateState(self):

        # Check mobility of the state
        legalMoves = self.GetLegalMoves()
        stateScore = -(len(legalMoves))

        # Check if a corner is available
        limit = self.size - 1
        corners = [(0, 0), (0, limit), (limit, 0), (limit, limit)]

        # Check if the current move is a corner play, or if the current state can allow for a corner play
        # Update both values
        for corner in corners:
            if corner in legalMoves:
                stateScore += -300.0

        return stateScore

    def IsLegal(self, move):
        """
        tells us if move is legal
        """
        if self.GetCaptures(move):
            return True
        return False

    def Play(self, p):
        """
        play at point p 
        """

        if isinstance(p, str):
            if p.lower() == 'pass':
                raise RuntimeError("passing during AB search, incorrect")
                self.current_player = opp(self.current_player)
                return True
            p = self.StrToPoint(p)
        
        captures = self.GetCaptures(p)
        if not captures:
            return False
        
        self.SetBoard(p[0], p[1], self.current_player)
        for x, y in captures:
            self.SetBoard(x, y, self.current_player)

        self.current_player = opp(self.current_player)
        self.move_history.append((p, captures))

        return True

    def Undo(self):
        """
        undo last move on the stack, and uncapture all captured pieces
        set captured to current player
        """
        p, captures = self.move_history.pop()
        x, y = p
        self.SetBoard(x, y, EMPTY)
        for x, y in captures:
            self.SetBoard(x, y, self.CurrentPlayer())
        self.current_player = opp(self.current_player)

    def Terminal(self):
        """
        return True if the game is over for the current state
        False otherwise
        """
        if self.GetLegalMoves():
            return False

        self.current_player = opp(self.current_player)
        if self.GetLegalMoves():
            self.current_player = opp(self.current_player)
            return False
        
        self.current_player = opp(self.current_player)
        return True

    def Winner(self):
        """
        return Winner, Score of the game
        """
        bcount = 0
        wcount = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.AccessBoard(i, j) == BLACK:
                    bcount += 1
                elif self.AccessBoard(i, j) == WHITE:
                    wcount += 1

        score = bcount - wcount + self.komi # komi to make sure we don't tie for now
        if score > 0:
            return BLACK, score
        elif score < 0:
            return WHITE, score
        else:
            raise ValueError("TIE OCCURRED WITH KOMI")
            return EMPTY, score

    def Hash(self):
        """
        return hash of the board's state (not including history)
        """
        return hash(self)

    def Place(self, point, color):
        """
        place a piece without checking legality.
        replaces currently placed pieces
        """
        assert(color in [BLACK, WHITE, EMPTY])
        r, c = point
        self.SetBoard(r, c, color)

    def GetLegalMoves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.IsLegal((i, j)):
                    moves.append((i, j))
        return [self.PointToStr(m) for m in moves]
