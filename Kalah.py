from Side import Side


class Kalah(object):
    def __init__(self, board):
        if board is None:
            raise TypeError("Board is null.")
        self.board = board

    def getBoard(self):
        return self.board

    """
  Checks whether a given move is legal on the underlying board. The move
  is not actually made.
  """

    def isLegalMove(self, move):
        return self.isLegalMoveOnBoard(self.board, move)

    """
  Performs a move on the underlying board. The move must be legal. If
  the move terminates the game, the remaining seeds of the opponent are
  collected into their store as well (so that all holes are empty).<BR>
  The "notifyObservers()" method of the board is called with the "move"
  as argument.
  """

    def makeMove(self, move):
        return self.makeMoveOnBoard(self.board, move)

    # Checks whether the game is over (based on the board).
    def gameOver(self):
        return self.gameOverOnBoard(self.board)

    """
    Checks whether a given move is legal on a given board. The move
    is not actually made.
  """

    def isLegalMoveOnBoard(self, board, move):
        return (move.getHole() <= board.getNoOfHoles()) and (board.getSeeds(move.getSide(), move.getHole()) != 0)

    """
    Performs a move on a given board. The move must be legal. If
    the move terminates the game, the remaining seeds of the opponent are
    collected into their store as well (so that all holes are empty).<BR>
    The "notifyObservers()" method of the board is called with the "move"
    as argument.
  """

    def makeMoveOnBoard(self, board, move):
        """
    1. The counters are lifted from this hole and sown in anti-clockwise direction, starting
        with the next hole. The player's own kalahah is included in the sowing, but the
        opponent's kalahah is skipped.
    2. outcome:
        1. if the last counter is put into the player's kalahah, the player is allowed to
           move again (such a move is called a Kalah-move);
        2. if the last counter is put in an empty hole on the player's side of the board
           and the opposite hole is non-empty,
           a capture takes place: all stones in the opposite opponents pit and the last
           stone of the sowing are put into the player's store and the turn is over;
        3. if the last counter is put anywhere else, the turn is over directly.
    3. game end:
        The game ends whenever a move leaves no counters on one player's side, in
        which case the other player captures all remaining counters. The player who
        collects the most counters is the winner."
    """

        seedsToSow = board.getSeeds(move.getSide(), move.getHole())
        board.setSeeds(move.getSide(), move.getHole(), 0)

        holes = board.getNoOfHoles()
        receivingPits = 2 * holes + 1  # sow into: all holes + 1 store
        rounds = int(seedsToSow / receivingPits)  # sowing rounds
        extra = seedsToSow % receivingPits  # seeds for the last partial round

        """
    the first "extra" number of holes get "rounds"+1 seeds, the
    remaining ones get "rounds" seeds
    """

        # sow the seeds of the full rounds (if any):
        if rounds != 0:
            for hole in range(1, holes + 1):
                board.addSeeds(Side.NORTH, hole, rounds)
                board.addSeeds(Side.SOUTH, hole, rounds)
            board.addSeedsToStore(move.getSide(), rounds)

        # sow the extra seeds (last round):
        sowSide = move.getSide()
        sowHole = move.getHole()  # 0 means store;

        for extra in range(extra, 0, -1):
            sowHole += 1
            if sowHole == 1:  # last pit was a store
                sowSide = Side.opposite(sowSide)
            if sowHole > holes:
                if sowSide == move.getSide():
                    sowHole = 0  # sow to the store now
                    board.addSeedsToStore(sowSide, 1)
                    continue
                else:
                    sowSide = Side.opposite(sowSide)
                    sowHole = 1

            # sow to hole
            board.addSeeds(sowSide, sowHole, 1)

        # capture:
        # last seed was sown on the moving player's side and not into the store
        if sowSide == move.getSide() and sowHole > 0 and board.getSeeds(sowSide, sowHole) == 1 and board.getSeedsOp(
                sowSide, sowHole) > 0:  # and the opposite hole is non-empty

            board.addSeedsToStore(move.getSide(), 1 + board.getSeedsOp(move.getSide(), sowHole))
            board.setSeeds(move.getSide(), sowHole, 0)
            board.setSeedsOp(move.getSide(), sowHole, 0)

        # game over?
        finishedSide = None
        if self.holesEmpty(board, move.getSide()):
            finishedSide = move.getSide()
        elif self.holesEmpty(board, Side.opposite(move.getSide())):
            finishedSide = Side.opposite(move.getSide())

        # note: it is possible that both sides are finished, but then
        # there are no seeds to collect anyway
        if finishedSide is not None:

            # collect the remaining seeds:
            seeds = 0
            collectingSide = Side.opposite(finishedSide)
            for hole in range(1, holes + 1):
                seeds += board.getSeeds(collectingSide, hole)
                board.setSeeds(collectingSide, hole, 0)

            board.addSeedsToStore(collectingSide, seeds)

        # whose turn is it?
        if sowHole == 0:  # the store (implies (sowSide == move.getSide()))
            return move.getSide()  # move again
        else:
            return Side.opposite(move.getSide())

    # Checks whether all holes on a given side are empty.
    def holesEmpty(self, board, side):
        for hole in range(1, board.getNoOfHoles() + 1):
            if board.getSeeds(side, hole) != 0:
                return False

        return True

    # Checks whether the game is over (based on the board).
    def gameOverOnBoard(self, board):
        # The game is over if one of the agents can't make another move.
        return self.holesEmpty(board, Side.SOUTH) or self.holesEmpty(board, Side.NORTH)
