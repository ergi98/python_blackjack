from constants import PLAYER_DECISION

from random import choice

class Hand():
  def __init__(self, is_real, is_dealer, is_split):
    self.cards = []
    self.score = 0
    self.decisions = []
    self.bet_amount = 0
    self.is_final = False
    self.is_real = is_real
    self.is_split = is_split
    self.is_dealer = is_dealer
    
  def split_hand(self):
    return ([self.cards[0]], [self.cards[1]])
    
  def bet(self, amount):
    self.bet_amount += amount
    
  def double_bet(self):
    self.bet_amount *= 2
  
  def calculate_hand_value(self):
    self.score = 0
    for card in self.cards:
      # All cases but the A (Ace)
      if isinstance(card.value, int):
        self.score += card.value
        continue
      # We have hit an ace
      one_value, eleven_value = card.value
      if self.score + eleven_value <= 21:
        self.score += eleven_value
      else:
        self.score += one_value
        
    if self.score >= 21:
      self.mark_hand_as_final()
      
  def mark_hand_as_final(self):
    self.is_final = True
 
  def add_to_hand(self, cards):
    self.cards.extend(cards)
    self.calculate_hand_value()
    
    
  def get_available_decisions(self, remaining_amount):
    available_decisions = []
    last_decision = ''
    with_insufficient_amount = self.bet_amount * 2 > remaining_amount
    try:
      last_decision = self.decisions[-1]
    except IndexError:
      pass
    # If hand is final or the last decision was double_down we can no longer make any decisions on the hand
    if self.is_final or last_decision == PLAYER_DECISION['DOUBLE_DOWN']:
      return available_decisions
    
    for decision in PLAYER_DECISION:
      # You can only decide to split once
      # You can only decide to split pairs
      # You can not split if you can not match the original bet on the new hand
      if (decision == 'SPLIT' and (self.is_split or with_insufficient_amount or self.cards[0] != self.cards[1])):
        continue;
      # You can only double down if you can double your initial bet
      elif decision == 'DOUBLE_DOWN' and with_insufficient_amount:
        continue;
      available_decisions.append(decision)
      
    return available_decisions
    
    
  def get_decision_prompt(self, decisions):
    decision_instructions = []
    for decision_key, decision_value in PLAYER_DECISION.items():
      if not decision_key in decisions:
        continue
      decision_instructions.append(f'{decision_value} to {decision_key.capitalize()}')
      
    return f'Press {', '.join(decision_instructions)}: '
  
  def from_value_to_key(self, value):
    for decision_key, decision_value in PLAYER_DECISION.items():
      if decision_value == value:
        return decision_key
      
    
  def prompt_for_decision(self, remaining_amount):
    user_decision = ''
    available_decisions = self.get_available_decisions(remaining_amount)
    
    while not user_decision in available_decisions:
      print(f'Your turn to decide for hand {str(self)}')
      # User
      user_decision = input(self.get_decision_prompt(decisions=available_decisions))
      user_decision = self.from_value_to_key(user_decision)
      
    return user_decision
      
  def get_decision(self, remaining_amount, player_name):
    decision = None
    # If hand is bust or blackjack no need for a further decision
    if self.is_final:
      return decision
    # If real user prompt for decision
    elif self.is_real:
      decision = self.prompt_for_decision(remaining_amount)
    # If bot decide randomly
    else:
      available_decisions = self.get_available_decisions(remaining_amount)
      decision = choice(available_decisions)
      
    if not decision == None:
      print(f'{player_name} decided to {decision.lower()} on hand {str(self)}')
      self.decisions.append(decision)
    
    return decision
    
  def __str__(self):
    return f'{','.join(map(lambda x: str(x), self.cards))} ({self.score})'
      