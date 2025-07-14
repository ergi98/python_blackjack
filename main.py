from game import Game

def main():
  blackjack_game = Game()
  blackjack_game.start_game()
  blackjack_game.place_initial_bets()
  
  while not blackjack_game.is_round_over():
    blackjack_game.deal_initial_cards()
    blackjack_game.go_round_the_table()
  
  pass;

if __name__ == "__main__":
  main();