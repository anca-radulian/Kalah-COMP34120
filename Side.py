from enum import Enum


class Side(Enum):
    NORTH = 1
    SOUTH = 0
    """
    @return the side opposite to this one.
    """

    def __init__(self):
        self.mySide = self.NORTH

    def opposite(self):
        if self == self.NORTH:
            return self.SOUTH
        elif self == self.SOUTH:
            return self.NORTH
        else:
            return self.NORTH

    def myTurn(self, side):
        return side == Side.mySide

    def setSouth(self):
        Side.mySide = Side.SOUTH

    def setNorth(self):
        Side.mySide = Side.NORTH