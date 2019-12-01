from Side import Side
from InvalidMessageException import InvalidMessageException
from MsgType import MsgType


class MoveTurn:
    end = False
    again = False
    move = 0


class Protocol:

    def createMoveMsg(self, hole):
        return "MOVE" + hole + '\n'

    def createSwapMsg(self):
        return "SWAP\n"

    """
     * Determines the type of a message received from the game engine. This
     * method does not check whether the message is well-formed.
     * @param msg The message.
     * @return The message type.
     * @throws InvalidMessageException if the message type cannot be
     *         determined.
     *
     """

    def getMessageType(self, msg):
        if msg.startswith("START;"):
            return MsgType.START
        elif msg.startswith("CHANGE;"):
            return MsgType.STATE
        elif msg.startswith("END\n"):
            return MsgType.END
        else:
            raise ValueError("Could not determine message type.")

    """
     * @param msg The message.
     * @return "true" if this agent is the starting player (South), "false"
     *         otherwise.
     * @throws InvalidMessageException if the message is not well-formed.
     * @see #getMessageType(String)
     *
     """

    def interpretStartMsg(self, msg):
        if msg[-1] != '\n':
            raise InvalidMessageException("Message not terminated with 0x0A character.")
        position = msg[6:-1]
        if position == 'South':
            return True
        elif position == 'North':
            return False
        else:
            raise InvalidMessageException("Illegal position parameter: " + str(position))

    """
     * Interprets a "state_change" message. Should be called if
     * getMessageType(msg) returns MsgType.STATE
     * @param msg The message.
     * @param board This is an output parameter. It will store the new state
     *        of the Kalah board. The board has to have the right dimensions
     *        (number of holes), otherwise an InvalidMessageException is
     *        thrown.
     * @return information about the move that led to the state change and
     *         who's turn it is next.
     * @throws InvalidMessageException if the message is not well-formed.
     * @see #getMessageType(String)
     """

    def interpretStateMsg(self, msg, board):
        moveTurn = MoveTurn()

        if msg[-1] != '\n':
            raise InvalidMessageException('Message not terminated with 0x0A character.')

        if len(msg.split(';', 4)) != 4:
            raise InvalidMessageException('Missing arguments.')

        msgParts = msg.split(';', 4)
        if msgParts[1] == 'SWAP':
            moveTurn.move = -1
        else:
            try:
                moveTurn.move = int(msgParts[1])
            except ValueError as e:
                raise InvalidMessageException('Illegal value for move parameter:' + str(e))

        boardParts = msgParts[2].split(',', - 1)
        if 2 * board.getNoOfHoles() + 1 != len(boardParts):
            raise InvalidMessageException(
                'Board dimensions in message (' + str(len(boardParts)) + 'entries) are not as expected (' + str(
                    2 * board.getNoOfHoles() + 1) + 'entries')

        try:
            for i in range(0, board.getNoOfHoles()):
                board.setSeeds(Side.NORTH, i + 1, int(boardParts[i]))
            board.setSeedsInStore(Side.NORTH, int(boardParts[board.getNoOfHoles()]))

            for i in range(0, board.getNoOfHoles()):
                board.setSeeds(Side.SOUTH, i + 1, int(i + boardParts[i]))
            board.setSeedsInStore(Side.SOUTH, int(boardParts[2 * board.getNoOfHoles() + 1]))
        except ValueError:
            print('Invalid value for seed count')

        moveTurn.end = False
        if msgParts[3] == 'YOU\n':
            moveTurn.again = True
        elif msgParts[3] == 'OPP\n':
            moveTurn.again = False
        elif msgParts[3] == 'END\n':
            moveTurn.end = True
            moveTurn.again = False
        else:
            raise InvalidMessageException('Illegal value for turn parameter:' + msgParts[3])

        return moveTurn
