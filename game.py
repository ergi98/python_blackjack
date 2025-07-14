from dealer import Dealer
from player import Player
from constants import MIN_PLAYER_COUNT, MAX_PLAYER_COUNT, PLAYER_NAMES

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
    print(f'Table players are: {', '.join(map(lambda player: player.name, self.players))}.')
    
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
    self.dealer.add_to_hand(cards=dealt_cards, hand=0)
  
  def place_initial_bets(self):
    for player in self.players:
      player.place_initial_bet()
  
  def go_round_the_table(self):
    '''
    Prompt each player to perform an action
    '''
    for player in self.players:
      player.get_hand_decisions(self.dealer)