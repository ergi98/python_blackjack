from deck import Deck
from hand import Hand

class Dealer():
  def __init__(self):
    self.deck = Deck() 
    self.hands = []
 
  def deal_card(self):
    return self.deck.draw_top_card()
  
  def add_to_hand(self, cards, hand):
    # Maximum number of hands is 2
    if hand > 1:
      raise Exception("Hand index greater than max number of hands allowed (2)")
    try:
      # In case the hand is already defined in that index push new card
       self.hands[hand].add_to_hand(cards)
    except IndexError:
      # If we get thrown an index error, create the hand and then assign card
      self.hands.append(Hand(is_real=False, is_dealer=True, is_split=False))
      self.hands[hand].add_to_hand(cards)
    
    print(f'Dealer: {' | '.join(map(lambda x: str(x), self.hands))}')
    