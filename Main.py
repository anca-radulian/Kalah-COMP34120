#!/usr/bin/python3

import sys
from Board import Board
from Kalah import Kalah
from Side import Side
from Move import Move
from MsgType import MsgType
from Protocol import Protocol
from InvalidMessageException import InvalidMessageException
from IOException import IOException
from Minimax import Minimax

"""
The main application class. It also provides methods for communication
with the game engine.
"""


# Sends a message to the game engine.
def sendMsg(msg):
    print(msg)
    sys.stdout.flush()

# Receives a message from the game engine.
def recvMsg():
    msg = sys.stdin.readline()
    return msg

# The main method, invoked when the program is started.
def main():
    try:
        board = Board(7, 7)
        mySide = Side.SOUTH
        n = 1
        while (True):
            recvmsg = recvMsg()
            try:
                protocol = Protocol()
                messType = protocol.getMessageType(recvmsg)
                if messType == MsgType.START:
                    interpretStartMsg = protocol.interpretStartMsg(recvmsg)
                    mySide = Side.SOUTH if interpretStartMsg else Side.NORTH
                    if interpretStartMsg:
                        n = 0
                        move = calculateNextBestMove(board, mySide)
                        sendMsg(protocol.createMoveMsg(move))
                        continue
                    continue
                elif messType == MsgType.STATE:
                    interpretStateMsg = protocol.interpretStateMsg(recvmsg, board)
                    if interpretStateMsg.again and interpretStateMsg.move == -1:  # if opponent does swap
                        mySide = Side.opposite(mySide)
                        move = calculateNextBestMove(board, mySide)
                        sendMsg(protocol.createMoveMsg(move))
                    elif interpretStateMsg.again and n != 0:  # if we swap
                        if interpretStateMsg.move <= 2:
                            mySide = Side.opposite(mySide)
                            sendMsg(protocol.createSwapMsg())  # Stab
                        else:
                            move = calculateNextBestMove(board, mySide)
                            sendMsg(protocol.createMoveMsg(move))
                    elif interpretStateMsg.again:
                        move = calculateNextBestMove(board, mySide)
                        sendMsg(protocol.createMoveMsg(move))
                    n = 0
                    continue
                else:
                    break
            except InvalidMessageException:
                invalidMessage = InvalidMessageException("Invalid move")
                print(invalidMessage.getMessage())
    except IOException:
        ioExceptionMessage = IOException("IOException")
        print(ioExceptionMessage.getMessage())


# returns the move
def calculateNextBestMove(board, side):
    scores = [-9999] * 8
    maxScore = -9999
    maxScoreIndex = -1
    kalah = Kalah(board)
    for i in range(1, 8):
        move = Move(side, i)
        if kalah.isLegalMove(move):
            newKalah = Kalah(board.copyBoard(board))
            newKalah.makeMove(move)
            scores[i] = Minimax(side).minimax(newKalah, -9999, 9999, side, 8)

        if maxScore < scores[i]:
            maxScoreIndex = i
            maxScore = scores[i]

    return maxScoreIndex


main()
