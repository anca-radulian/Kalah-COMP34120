from enum import Enum


class Side(Enum):
    NORTH = 1
    SOUTH = 0
    """
    @return the side opposite to this one.
    """

    def opposite(self):
        if self == self.NORTH:
            return self.SOUTH
        elif self == self.SOUTH:
            return self.NORTH
        else:
            return self.NORTH
