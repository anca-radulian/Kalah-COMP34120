class Side(object):
    NORTH = 1
    SOUTH = 0

    def __init__(self):
        self.side = self.NORTH
    """
    @return the side opposite to this one.
    """
    def opposite(self):
        if self.side == self.NORTH:
            return self.SOUTH
        elif self.side == self.SOUTH:
            return self.NORTH
        else:
            return self.NORTH

    def myTurn(self, side):
        return side.side == self.side

    def setSouth(self):
        self.side = self.SOUTH

    def setNorth(self):
        self.side = self.NORTH
