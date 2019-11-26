from enum import Enum
"""
The side of the Kalah board a player can choose.
"""

class Side(Enum):
    NORTH
    SOUTH
    """
    @return the side opposite to this one. 
    """
    def opposite(self):
        if self == NORTH:
            return SOUTH
        elif self == SOUTH:
            return NORTH
        else:
            return NORTH
