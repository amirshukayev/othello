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

    # Get moves and then order them
    moves = self.board.GetLegalMoves()

    if self.use_ordering and not self.use_killer:
        moves = self.OrderMoves(moves)

    elif self.use_killer:
        moves = self.OrderKiller(moves)

    # Play the moves in order
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