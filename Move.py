import Side

# Represents a move (not a turn) in the Kalah game.
class Move:

  # The side of the board the player making the move is playing on.
  _side = []
  _hole = 1
  
  """
   side = The side of the board the player making the move is playing on.
   hole = The hole from which seeds are picked at the beginning of
   the move and distributed. It has to be >= 1.
  """
  def _init_(self, side, hole):
    if hole < 1:
      raise ValueError('Hole numbers must be >= 1, but ' + hole + ' was given.')

    self.side = side
    self.hole = hole

  def getSide(self):
    return self.side

  def getHole(self):
    return self.hole
