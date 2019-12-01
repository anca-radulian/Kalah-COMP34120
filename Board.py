"""
 Representation of the Kalah board.
 The board has two sides: "North" and
 "South". On each side there is a number of linearly arranged "holes" (the
 same number on each side) and a "store" for each side. Holes are numbered
 per side, starting with 1 on "the left" (i.e. furthest away from the
 player's store, the numbers increase in playing direction).

 Initially, there is the same number of "seeds" in each hole.
"""


class Board:
    """
    @see #board
    """
    NORTH_ROW = 0
    SOUTH_ROW = 1

    """
    The board data. The first dimension of the array is 2, the second one
    is the number of holes per side plus one. The data for the North side
    is stored in board[NORTH_ROW][*], the data for the South side in
    board[SOUTH_ROW][*]. The number of seeds in hole number n (of one side)
    is stored in board[...][n], the number of seeds in the store (of one
    side) is stored in board[...][0].
    """

    """
    @param side A side of the board.
    @return The index of side "side" for the first dimension of "board".
    """

    def indexOfSide(self, side):
        if side == side.NORTH:
            return self.NORTH_ROW
        elif side == side.NORTH:
            return self.SOUTH_ROW
        else:
            return -1

    """
     Creates a new board.
    
     @param holes The number of holes per side (must be >= 1).
     @param seeds The initial number of seeds per hole (must be >= 0). The
            stores are empty initially.
     @throws IllegalArgumentException if any of the arguments is outside of
             the valid range.
    """

    def __init__(self, currentHoles, currentSeeds):
        if currentHoles < 1:
            raise Exception("There has to be at least one hole, but " + currentHoles + " were requested.")
        if currentSeeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + currentSeeds + " were requested.")

        self.holes = currentHoles
        self.board = [[0 for y in range(currentHoles + 1)] for y in range(currentHoles + 1)]
        for i in range(1, currentHoles + 1, 1):
            self.board[self.NORTH_ROW][i] = currentSeeds
            self.board[self.SOUTH_ROW][i] = currentSeeds

    """
     Creates a new board as the copy of a given one. Both copies can then be
     altered independently.
    
     @param original The board to copy.
     @see #clone()
    """

    def copyBoard(self, original):
        self.holes = original.holes
        self.board = [[0 for x in range(2)] for y in range(self.holes + 1)]

        for i in range(1, self.holes + 1, 1):
            self.board[self.NORTH_ROW][i] = original.board[self.NORTH_ROW][i]
            self.board[self.SOUTH_ROW][i] = original.board[self.SOUTH_ROW][i]

    """
     Creates a copy of the current board. Both copies can then be altered
     independently.
    
     @see java.lang.Object#clone()
     @see #Board(Board)
    """

    def clone(self):
        return self.copyBoard(self)

    """
     @return The number of holes per side (will be >= 1).
    """

    def getNoOfHoles(self):
        return self.holes

    """
     Get the number of seeds in a hole.
     @param side The side the hole is located on.
     @param hole The number of the hole.
     @return The number of seeds in hole "hole" on side "side".
     @throws IllegalArgumentException if the hole number is invalid.
    """

    def getSeeds(self, side, hole):
        if hole < 1 or hole > self.holes:
            numberOfHoles = len(self.board[self.NORTH_ROW])
            raise Exception(
                "Hole number must be between 1 and " + str(numberOfHoles) + " but was " + hole + ".")

        return self.board[self.indexOfSide(side)][hole]

    """
     Sets the number of seeds in a hole.
     @param side The side the hole is located on.
     @param hole The number of the hole.
     @param seeds The number of seeds that shall be in the hole afterwards (>= 0).
     @throws IllegalArgumentException if any of the arguments is outside of
             the valid range.
    """

    def setSeeds(self, side, hole, seeds):
        if hole < 1 or hole > self.holes:
            numberOfHoles = len(self.board[self.NORTH_ROW])
            raise Exception(
                "Hole number must be between 1 and " + str(numberOfHoles) + " but was " + hole + ".")
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[self.indexOfSide(side)][hole] = seeds

    """
     Adds seeds to a hole.
     @param side The side the hole is located on.
     @param hole The number of the hole.
     @param seeds The number (>= 0) of seeds to put into (add to) the hole.
     @throws IllegalArgumentException if any of the arguments is outside of
             the valid range.
    """

    def addSeeds(self, side, hole, seeds):
        if hole < 1 or hole > self.holes:
            numberOfHoles = len(self.board[self.NORTH_ROW])
            raise Exception(
                "Hole number must be between 1 and " + str(numberOfHoles) + " but was " + hole + ".")
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[self.indexOfSide(side)][hole] += seeds

    """
     Get the number of seeds in a hole opposite to a given one.
     @param side The side the given hole is located on.
     @param hole The number of the given hole.
     @return The number of seeds in the hole opposite to hole "hole" on
             side "side".
     @throws IllegalArgumentException if the hole number is invalid.
    """

    def getSeedsOp(self, side, hole):
        if hole < 1 or hole > self.holes:
            raise Exception("Hole number must be between 1 and " + self.holes + " but was " + hole + ".")

        return self.board[1 - self.indexOfSide(side)][self.holes + 1 - hole]

    """
     Sets the number of seeds in a hole opposite to a given one.
     @param side The side the given hole is located on.
     @param hole The number of the given hole.
     @param seeds The number of seeds that shall be in the hole opposite to
            hole "hole" on side "side" afterwards (>= 0).
     @throws IllegalArgumentException if any of the arguments is outside of
             the valid range.
    """

    def setSeedsOp(self, side, hole, seeds):
        if hole < 1 or hole > self.holes:
            numberOfHoles = len(self.board[self.NORTH_ROW])
            raise Exception(
                "Hole number must be between 1 and " + str(numberOfHoles) + " but was " + hole + ".")
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[1 - self.indexOfSide(side)][self.holes + 1 - hole] = seeds

    """
     Adds seeds to a hole opposite to a given one.
     @param side The side the given hole is located on.
     @param hole The number of the given hole.
     @param seeds The number (>= 0) of seeds to put into (add to) the hole opposite to
            hole "hole" on side "side" afterwards (>= 0).
     @throws IllegalArgumentException if any of the arguments is outside of
             the valid range.
    """

    def addSeedsOp(self, side, hole, seeds):
        if hole < 1 or hole > self.holes:
            numberOfHoles = len(self.board[self.NORTH_ROW])
            raise Exception(
                "Hole number must be between 1 and " + str(numberOfHoles) + " but was " + hole + ".")
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[1 - self.indexOfSide(side)][self.holes + 1 - hole] += seeds

    """
     Get the number of seeds in a store.
     @param side The side the store is located on.
     @return The number of seeds in the store.
    """

    def getSeedsInStore(self, side):
        return self.board[self.indexOfSide(side)][0]

    """
     Sets the number of seeds in a store.
     @param side The side the store is located on.
     @param seeds The number of seeds that shall be in the store afterwards (>= 0).
     @throws IllegalArgumentException if the number of seeds is invalid.
    """

    def setSeedsInStore(self, side, seeds):
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[self.indexOfSide(side)][0] = seeds

    """
     Adds seeds to a store.
     @param side The side the store is located on.
     @param seeds The number (>= 0) of seeds to put into (add to) the store.
     @throws IllegalArgumentException if the number of seeds is invalid.
    """

    def addSeedsToStore(self, side, seeds):
        if seeds < 0:
            raise Exception("There has to be a non-negative number of seeds, but " + seeds + " were requested.")

        self.board[self.indexOfSide(side)][0] += seeds

    def __str__(self):
        boardString = ""

        boardString += str(self.board[self.NORTH_ROW][0]) + "  --"
        for i in range(self.holes, 0, -1):
            boardString += "  " + str(self.board[self.NORTH_ROW][i])
        boardString += "\n"
        for i in range(1, self.holes + 1, 1):
            boardString += str(self.board[self.SOUTH_ROW][i]) + "  "
        boardString += "--  " + str(self.board[self.SOUTH_ROW][0]) + "\n"

        return boardString
