from constants import POINT_SYSTEM 

class Card():
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
    self.value = POINT_SYSTEM[rank]
    
  def __str__(self):
    return f'{self.rank}{self.suit[0]}'