from Move import Move
from Kalah import Kalah
from Side import Side


class Minimax:
    isPreviousMoveFromRightMostHole = 0

    def __init__(self, side):
        self.mySide = side

    def alphabeta(self, kalahBoard, alpha, beta, side, depth):
        board = kalahBoard.getBoard()

        if kalahBoard.gameOver() or depth <= 0:
            value = self.evalHeuristics(kalahBoard.getBoard(), side, self.isPreviousMoveFromRightMostHole)
        elif side == self.mySide:
            value = - 9999  # -INF
            for i in range(1, 8):
                boardCopy = board.copyBoard(board)
                kalahCopy = Kalah(boardCopy)
                move = Move(side, i)

                if kalahCopy.isLegalMove(move):
                    self.isPreviousMoveFromRightMostHole = self.isMoveFromRightMostHole(board, side, move.getHole())
                    nextSide = kalahCopy.makeMove(move)

                    value = max(value, self.alphabeta(kalahCopy, alpha, beta, nextSide, depth - 1))
                    alpha = max(value, alpha)

                    if alpha >= beta:
                        break
                    else:
                        alpha = -999  # -INF ?? penalize no moves

        else:  # opponent
            value = 9999  # INF

            for i in range(1, 8):
                boardCopy = board.copyBoard(board)
                kalahCopy = Kalah(boardCopy)
                move = Move(side, i)

                if kalahCopy.isLegalMove(move):
                    nextSide = kalahCopy.makeMove(move)
                    value = min(value, self.alphabeta(kalahCopy, alpha, beta, nextSide, depth - 1))
                    beta = min(value, beta)

                    if alpha >= beta:
                        break
                    else:
                        beta = 999

        return value

    def evalHeuristics(self, board, side, previousMove):
        w1 = 0.198649
        w2 = 0.190084
        w3 = 0.370793
        w4 = 1
        w5 = 0.418841
        w6 = 0.565937

        h1 = self.hoardInLeftmostHole(board, side)
        h2 = self.hoardOnMySide(board, side)
        h3 = self.possibleMoves(board, side)
        h4 = self.seedsInStore(board, side)
        h5 = self.isPreviousMoveFromRightMostHole
        h6 = self.seedsInStore(board, Side.opposite(side))

        return h1 * w1 + w2 * h2 + h3 * w3 + h4 * w4 + h5*w5 - h6 * w6

    def seedsInStore(self, board, side):
        # Calculate a score based on how many seeds are in the store based on the move
        score = board.getSeedsInStore(side)
        return score

    def hoardInLeftmostHole(self, board, side):
        # Calculate the score based on how many seeds there are in the leftmost hole.
        score = board.getSeeds(side, 1)
        return score

    def hoardOnMySide(self, board, side):
        # Calculate the score based on how many seeds there are on my side.
        score = 0

        for i in range(1, 8):
            score += board.getSeeds(side, i)

        return score

    def possibleMoves(self, board, side):
        # Calculate how many holes are not empty
        score = 0

        for i in range(1, 8):
            if board.getSeeds(side, i) != 0:
                score += 1
        return score

    def isMoveFromRightMostHole(self, board, side, move):
        result = 0

        for i in range(7, 0, -1):
            if board.getSeeds(side, i) != 0:
                if move == i:
                    result = 1
                break
        return result
