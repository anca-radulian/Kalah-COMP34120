from Move import Move
from Kalah import Kalah
from Side import Side


class Minimax:

    isPreviousMoveFromLeft = 0
    isPreviousMoveFromRight = 0

    def __init__(self, side):
        self.mySide = side

    def minimax(self, kalah_board, alpha, beta, side, depth):
        board = kalah_board.getBoard()
        if depth == 0 or kalah_board.gameOver():
            return self.evalHeuristics(kalah_board.getBoard())

        if side == self.mySide:
            max_evaluation = - 9999
            self.isPreviousMoveFromLeft = 1
            for possible_move in range(1, 8):
                board_copy = board.copyBoard(board)
                kalah_copy = Kalah(board_copy)
                move = Move(side, possible_move)
                if kalah_copy.isLegalMove(move):
                    self.isPreviousMoveFromRight = self.isMoveFromRightMostHole(board_copy, side, possible_move)
                    nextSide = kalah_copy.makeMove(move)
                    evaluation = self.minimax(kalah_copy, alpha, beta, nextSide, depth - 1)
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
                    self.isPreviousMoveFromLeft = 0
            return max_evaluation
        else:
            min_evaluation = 9999
            for possible_move in range(1, 8):
                board_copy = board.copyBoard(board)
                kalah_copy = Kalah(board_copy)
                move = Move(side, possible_move)
                if kalah_copy.isLegalMove(move):
                    nextSide = kalah_copy.makeMove(move)
                    evaluation = self.minimax(kalah_copy, alpha, beta, nextSide, depth - 1)
                    min_evaluation = min(min_evaluation, evaluation)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
            return min_evaluation

    def evalHeuristics(self, board):
        # Weights depth 9
        w1 = 0.675
        w2 = 0.275
        w3 = 0.675
        w4 = 1
        w5 = 0.5
        w6 = 0.7
        w7 = 0.475

        h1 = self.hoardInLeftmostHole(board, self.mySide)
        h2 = self.hoardOnMySide(board, self.mySide)
        h3 = self.possibleMoves(board, self.mySide)
        h4 = self.seedsInStore(board, self.mySide)
        h5 = self.isPreviousMoveFromRight
        h6 = self.seedsInStore(board, Side.opposite(self.mySide))
        h7 = self.isPreviousMoveFromLeft

        return h1 * w1 + h2 * w2 + h3 * w3 + h4 * w4 + h5 * w5 - h6 * w6 + h7 * w7

    def isMoveFromLeftMostHole(self, board, side, move):
        result = 0

        for i in range(1, 8):
            if board.getSeeds(side, i) != 0:
                if move == i:
                    result = 1
                break
        return result

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
