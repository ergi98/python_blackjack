from game import Game
from colorama import Fore, Style

def print_player_hand_information(game):
  bet_info = []
  for player in game.players:
    player_bets = []
    for hand in player.hands:
      hand_str = str(hand)
      if hand_str == '':
        player_bets.append(f'{hand.bet_amount}$')
      else:
        player_bets.append(f'{hand.bet_amount}$ on {hand_str}')
      if player.is_real:
        bet_info.append(f'{Fore.GREEN}Your bets: {', '.join(player_bets)}{Style.RESET_ALL}')
      else:
        bet_info.append(f'{player.name} bets: {', '.join(player_bets)}')
  print(f'{" | ".join(bet_info)}')

def print_player_cash_amounts(game):
  cash_amounts = []
  for player in game.players:
    if player.is_real:
      cash_amounts.append(f'{Fore.GREEN}Your remaining amount: {player.cash_amount}${Style.RESET_ALL}')
    else:
      cash_amounts.append(f'{player.name}: {player.cash_amount}$')
  print(f'{" | ".join(cash_amounts)}')
  

def main():
  blackjack_game = Game()
  blackjack_game.start_game()
  
  while not blackjack_game.is_real_player_bankrupt():
    # Printing player remaining cash amounts
    print_player_cash_amounts(game=blackjack_game)
    blackjack_game.place_initial_bets()
    while not blackjack_game.is_round_over():
      blackjack_game.deal_initial_cards()
      # Printing player bets cash amounts
      print_player_hand_information(game=blackjack_game)
      blackjack_game.check_for_natural_blackjack_hands()
      blackjack_game.go_round_the_table()
      print_player_hand_information(game=blackjack_game)
      print("All players have decided on their hands. Dealer is drawing")
      blackjack_game.complete_dealer_hand()
      print(f'Dealer hand: {str(blackjack_game.dealer.hand)}')
      blackjack_game.decide_winners_and_losers()
      
      
    blackjack_game.remove_bankrupt_players()
    blackjack_game.setup_players_for_round_start()
    blackjack_game.setup_dealer_for_round_start()
  
if __name__ == "__main__":
  main();