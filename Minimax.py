from Move import Move
from Kalah import Kalah

class Minimax:
    def __init__(self, side):
        self.mySide = side

    def alphabeta(self, kalahBoard, alpha, beta, side, depth):
        board = kalahBoard.getBoard()

        if kalahBoard.gameOver() or depth <= 0:
            value = self.evalHeuristics(kalahBoard.getBoard())
        elif side == self.mySide:
            value = - 999  # -INF
            for i in range(1, 8):
                boardCopy = board.copyBoard(board)
                kalahCopy = Kalah(boardCopy)
                move = Move(side, i)

                if kalahCopy.isLegalMove(move):
                    nextSide = kalahCopy.makeMove(move)
                    value = max(value, self.alphabeta(kalahCopy, alpha, beta, nextSide, depth - 1))
                    alpha = max(value, alpha)

                    if alpha >= beta:
                        break
                    else:
                        alpha = -999  # -INF ?? penalize no moves

        else:  # opponent
            value = 999  # INF

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

    def evalHeuristics(self, board):
        # Calculate a score based on how many seeds are in the store based on the move
        score = board.getSeedsInStore()
        return score
