from deck import Deck
from hand import Hand

class Dealer():
  def __init__(self):
    self.deck = Deck() 
    self.hand = Hand(is_real=False, is_dealer=True, is_split=False)
 
  def deal_card(self):
    return self.deck.draw_top_card()
  
  def add_to_hand(self, cards):
    self.hand.add_to_hand(cards)
    
  def complete_hand(self):
    while self.hand.score < 17:
      card = self.deal_card()
      self.add_to_hand(cards=[card])
    
  def setup_for_round_start(self):
    self.deck = Deck()
    self.hand = Hand(is_real=False, is_dealer=True, is_split=False)