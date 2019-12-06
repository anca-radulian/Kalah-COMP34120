import math
import random
from Kalah import Kalah
class MCTS:
    def __init__(self,kalahBoard, side):
        self.kalahBoard = kalahBoard
        self.side = side

    def expansion(self, kalahBoard):
        board = kalahBoard.getBoard()
