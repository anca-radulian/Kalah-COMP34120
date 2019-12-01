from Side import Side
from Move import Move

class Minimax:
    def __init__(self, player):
      self.player = player

    def alphabeta(self, kalahBoard, board, alpha, beta, player, depth):
        value = 0

        if kalahBoard.gameOverOnBoard(board) or depth <= 0:
            value = self.evalHeuristics(board)
        elif player == self.player:
            value = - 999  # -INF

            for x in range(1, 8):
                boardCopy = board.copyBoard(board)
                side = Side()  # might return always North??
                move = Move(side, x)

                if kalahBoard.isLegalMove(boardCopy, move):
                    playerMove = kalahBoard.makeMove(boardCopy, move)
                    value = max(value, self.alphabeta(kalahBoard, boardCopy, alpha, beta, playerMove, depth - 1))
                    alpha = max(value, alpha)

                    if alpha >= beta:
                        break
                    else:
                        alpha = -999  # -INF ?? penalize no moves

        else:  # opponent
            value = 999  # INF

            for x in range(1, 8):
                boardCopy = board.copyBoard(board)
                side = Side()  # might return always North??
                move = Move(side.opposite(), x)

                if kalahBoard.isLegalMove(boardCopy, move):
                    playerMove = kalahBoard.makeMove(boardCopy, move)
                    value = min(value, self.alphabeta(kalahBoard, boardCopy, alpha, beta, playerMove, depth - 1))
                    beta = min(value, beta)

                    if alpha >= beta:
                        break
                    else:
                        beta = 999

        return value


    def evalHeuristics(self, board):
      return 0