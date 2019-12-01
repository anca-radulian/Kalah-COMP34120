import sys
from Board import Board
from Kalah import Kalah
from Side import Side
from Move import Move

"""
The main application class. It also provides methods for communication
with the game engine.
"""


# Sends a message to the game engine.
def sendMsg(msg):
    print(msg, flush=True)


# Receives a message from the game engine.
def recvMsg():
    msg = sys.stdin.readline()
    return msg


# The main method, invoked when the program is started.
def main():
    board = Board(7, 7)
    side = Side()
    side.setSouth()
    calculateNextBestMove(board, side)
    return 0


# returns the move
def calculateNextBestMove(board, side):
    scores = []
    maxScore = 0
    maxScoreIndex = 1
    kalah = Kalah(board)
    for i in range(1, 8, 1):
        move = Move(side, i)
        if kalah.isLegalMove(move):
            newKalah = Kalah(board.copyBoard(board))
            scores[i] = alphaBetaMiniMax(newKalah.makeMove(move))
        else:
            scores[i] = 0
        if maxScore < scores[i]:
            maxScoreIndex = i
            maxScore = scores[i]

    return maxScoreIndex


def alphaBetaMiniMax(board):
    return 0


main()
