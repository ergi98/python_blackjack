from dealer import Dealer
from player import Player
from constants import MIN_PLAYER_COUNT, MAX_PLAYER_COUNT, PLAYER_NAMES
from colorama import Fore, Style
from math import floor

class Game():
  def __init__(self):
    self.players = []
    self.dealer = Dealer()

  def is_number_of_players_valid(self, player_count):
    try:
      player_count_as_int = int(player_count)
      return player_count_as_int >= MIN_PLAYER_COUNT and player_count_as_int <= MAX_PLAYER_COUNT
    except:
      return False
    
  def add_user_player(self):
    name = input(f'Please enter your name: ')
    self.players.append(Player(name=name, is_real=True))
    
  def add_bot_players(self):
    player_count = -1
    while not self.is_number_of_players_valid(player_count):
      player_count = input(f'Number of bot players from {MIN_PLAYER_COUNT} to {MAX_PLAYER_COUNT}: ')
    for i in range(0, int(player_count)):
      self.players.append(Player(name=PLAYER_NAMES[i]))
    
  def start_game(self):
    '''
    Asks the user for information and fills the table with players
    '''
    self.add_user_player()
    self.add_bot_players()
    
  def is_round_over(self):
    for player in self.players:
      if player.with_open_hands():
        return False
    return True
  
  def deal_initial_cards(self):
    dealt_cards = []
    # Deal to players first
    for player in self.players:
      for _ in range (0, 2):
        dealt_cards.append(self.dealer.deal_card())
      player.add_to_hand(cards=dealt_cards, hand=0)
      dealt_cards.clear()
    # Deal to the dealer
    for _ in range (0, 2):
      dealt_cards.append(self.dealer.deal_card())
    self.dealer.add_to_hand(cards=dealt_cards)
  
  def place_initial_bets(self):
    for player in self.players:
      player.place_initial_bet()
  
  def go_round_the_table(self):
    '''
    Prompt each player to perform an action
    '''
    for player in self.players:
      player.get_hand_decisions(self.dealer)
      
  def complete_dealer_hand(self):
    '''
    Dealer must hit until his hand value is 17 or higher
    '''
    self.dealer.complete_hand()
    
  def decide_hand_outcome(self, player_hand, dealer_hand):
    # Bust hand is an automatic loss
    if player_hand.score > 21:
      return ('LOSS', 0)
    if dealer_hand.score > 21:
      return ('WIN', 1)
    if player_hand.score > dealer_hand.score:
      if player_hand.is_natural_blackjack:
        return ('WIN', 1.5)
      return ('WIN', 1)
    if player_hand.score == dealer_hand.score:
      return ('PUSH', 0)
    return ('LOSS', 0)
  
  def apply_hand_outcome(self, player, outcome, multiplier, bet):
    if outcome == 'LOSS':
      return;
    player.update_cash_amount(bet + bet * multiplier)

  def decide_winners_and_losers(self):
    '''
    Go over each player and 
    Pay winners
    For losers do nothing since cash is already subtracted when bet was placed
    For players with the same score as dealers return bet amount
    '''
    outcome_info = []
    for player in self.players:
      player_info = []      
      for hand in player.hands:
        hand_str = ''
        hand_outcome, win_multiplier = self.decide_hand_outcome(player_hand=hand, dealer_hand=self.dealer.hand)
        self.apply_hand_outcome(player=player, outcome=hand_outcome, multiplier=win_multiplier, bet=hand.bet_amount)
        # ONLY FOR STYLING
        if hand_outcome == 'WIN':
          hand_str += f'won on hand {str(hand)} {hand.bet_amount * win_multiplier}$'
        elif hand_outcome == 'PUSH':
          hand_str += f'got original bet back on hand'
        elif hand_outcome == 'LOSS':
          hand_str += f'lost on hand {str(hand)} {hand.bet_amount}$'
          
        if player.is_real:
          hand_str = f'{Fore.GREEN}You {hand_str}{Style.RESET_ALL}'
        else: 
          hand_str = f'{player.name} {hand_str}'
        player_info.append(hand_str)
      outcome_info.append(', '.join(player_info))
    print(f'{' | '.join(outcome_info)}')
     
  def check_for_natural_blackjack_hands(self):
    for player in self.players:
      for hand in player.hands:
        hand.check_if_natural_blackjack()
        
  def setup_players_for_round_start(self):
    for player in self.players:
      player.setup_for_round_start()
      
  def is_real_player_bankrupt(self):
    for player in self.players:
      if player.is_real and floor(player.cash_amount) >= 1:
        return False
    return True
  
  def setup_dealer_for_round_start(self):
    self.dealer.setup_for_round_start()
    
  def remove_bankrupt_players(self):
    self.players = list(filter(lambda x: x.is_real or floor(x.cash_amount) >= 1, self.players))