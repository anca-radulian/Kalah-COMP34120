from enum import Enum


class Side(Enum):
    NORTH = 1
    SOUTH = 0

    def opposite(side):
        if side == Side.NORTH:
            return Side.SOUTH
        elif side == Side.SOUTH:
            return Side.NORTH
        else:
            return Side.NORTH
