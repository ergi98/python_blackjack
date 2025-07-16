from hand import Hand

from random import randrange
from math import floor

class Player():
  def __init__(self, name, is_real=False):
    self.hands = []
    self.name = name
    self.cash_amount = 500
    self.is_real = is_real
    self.is_done_deciding = False
    
  def stand_on_hand(self, hand):
    self.hands[hand].mark_hand_as_final()
  
  def add_to_hand(self, cards, hand):
    # Maximum number of hands is 2
    if hand > 1:
      raise Exception("Hand index greater than max number of hands allowed (2)")
    # In case the hand is already defined in that index push new card
    self.hands[hand].add_to_hand(cards)
    
  def place_bet_on_hand(self, bet_amount):
    if not len(self.hands) == 0:
      raise Exception("Can not place bet on existing hand.")
    # Create hand
    self.hands.append(Hand(is_real=self.is_real, is_dealer=False, is_split=False))
    # Place bet
    self.hands[0].bet(bet_amount)
    self.cash_amount -= bet_amount
    
  def double_bet_on_hand(self, hand):
    self.cash_amount -= self.hands[hand].bet_amount
    self.hands[hand].double_bet()
    
  def split_hand(self, cards, hand):
    new_hands = self.hands[hand].split_hand()
    current_bet = self.hands[hand].bet_amount
    # Remove old hand
    self.hands.clear()
    # Splitting current hand in two new hands
    for i in range (0, 2):
      temp_hand = Hand(is_real=self.is_real, is_dealer=False, is_split=True)
      # Add card to new hand
      new_hands[i].append(cards[i])
      # Add a new card to complete the hand
      temp_hand.add_to_hand(new_hands[i])
      # Match the bet on both hands
      temp_hand.bet(current_bet)
      self.hands.append(temp_hand)
    # Remove from cash pool
    self.cash_amount -= current_bet
        
  def is_bet_valid(self, bet_amount):
    try:
      bet_amount_as_int = int(bet_amount)
      return bet_amount_as_int >= 1 and bet_amount_as_int <= self.cash_amount
    except:
      return False
    
  def place_initial_bet(self):
    if self.is_real:
      user_bet = ''
      while not self.is_bet_valid(user_bet):
        user_bet = input(f'Place your bet between 1$ and {self.cash_amount}$: ')
      user_bet = int(user_bet)
    else:
      user_bet = randrange(1, floor(self.cash_amount) + 1)
    self.place_bet_on_hand(bet_amount=user_bet)
    
  def mark_hand_as_final(self, hand):
    self.hands[hand].mark_hand_as_final()
    
  def with_open_hands(self):
    for hand in self.hands:
      if not hand.is_final:
        return True
    return False
      
  def get_hand_decisions(self, dealer):
    while self.with_open_hands():
      for hand_index, hand in enumerate(self.hands):
        while not hand.is_final:
          decision = hand.get_decision(remaining_amount=self.cash_amount, player_name=self.name)
          if decision == 'HIT':
            card = dealer.deal_card()
            self.add_to_hand(cards=[card], hand=hand_index)
          elif decision == 'STAND':
            self.stand_on_hand(hand=hand_index)
          elif decision == 'DOUBLE_DOWN':
            card = dealer.deal_card()
            self.add_to_hand(cards=[card], hand=hand_index)
            self.double_bet_on_hand(hand=hand_index)
            self.mark_hand_as_final(hand=hand_index)
            
          elif decision == 'SPLIT':
            cards = [dealer.deal_card(), dealer.deal_card()]
            self.split_hand(cards=cards, hand=hand_index)
            # Exit from the while loop
            break;
      
  def update_cash_amount(self, amount):
    self.cash_amount += amount
    
  def setup_for_round_start(self):
    self.hands.clear()
    self.is_done_deciding = False
