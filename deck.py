from card import Card
from constants import SUITS, POINT_SYSTEM
from random import shuffle

class Deck():
  def __init__(self):
    '''
		Fill the deck with all the cards
		'''
    self.cards = [];
    for suit in SUITS:
      # Iterating over the keys of the POINT_SYSTEM which coincide with the rank of the card
      for rank in POINT_SYSTEM:
        self.cards.append(Card(rank, suit))
    shuffle(self.cards)
    
  def is_empty(self):
    return len(self.cards) == 0
    
  def draw_top_card(self):
    return self.cards.pop()