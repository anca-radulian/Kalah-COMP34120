from Move import Move
from Kalah import Kalah
from Side import Side


class Minimax:

    def __init__(self, side):
        self.mySide = side

    def minimax(self, kalah_board, alpha, beta, side, depth):
        board = kalah_board.getBoard()
        if depth == 0 or kalah_board.gameOver():
            return self.evalHeuristics(kalah_board.getBoard(), side)

        if side == self.mySide:
            max_evaluation = - 9999
            for possible_move in range(1, 8):
                board_copy = board.copyBoard(board)
                kalah_copy = Kalah(board_copy)
                move = Move(side, possible_move)
                if kalah_copy.isLegalMove(move):
                    kalah_copy.makeMove(move)
                    evaluation = self.minimax(kalah_copy, alpha, beta, Side.opposite(side), depth - 1)
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
            return max_evaluation
        else:
            min_evaluation = 9999
            for possible_move in range(1, 8):
                board_copy = board.copyBoard(board)
                kalah_copy = Kalah(board_copy)
                move = Move(side, possible_move)
                if kalah_copy.isLegalMove(move):
                    kalah_copy.makeMove(move)
                    evaluation = self.minimax(kalah_copy, alpha, beta, Side.opposite(side), depth - 1)
                    min_evaluation = min(min_evaluation, evaluation)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
            return min_evaluation

    def evalHeuristics(self, board, side):
        w1 = 0.741
        w2 = 0.325
        w3 = 0.898
        w4 = 0.752
        w5 = 1
        w6 = 0.797
        w7 = 1


        h1 = self.hoardInLeftmostHole(board, side)
        h2 = self.hoardOnMySide(board, side)
        h3 = self.possibleMoves(board, side)
        h4 = self.seedsInStore(board, side)
        h5 = self.isMoveFromRightMostHole(board, side)
        h6 = self.seedsInStore(board, Side.opposite(side))
        h7 = self.move_first_possible(board, side)

        return h1 * w1 + h2 * w2 + h3 * w3 + h4 * w4 + h5 * w5 + h6 * w6 + h7 * w7

    def move_first_possible(self, board, side):
        copy_board = board
        score = 0
        for hole in range (1, 8):
            if not copy_board.getSeeds(side, hole) == 0:
                score = 1
        return score

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

    def isMoveFromRightMostHole(self, board, side):
        result = 0

        if board.getSeeds(side, 7) != 0:
            result = 1
        return result
