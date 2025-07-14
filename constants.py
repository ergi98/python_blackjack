SUITS = ("Heart", "Diamonds", "Clubs", "Spades")
POINT_SYSTEM = {
  '2': 2,
  '3': 3,
  '4': 4,
  '5': 5,
  '6': 6,
  '7': 7,
  '8': 8,
  '9': 9,
  '10': 10,
  'J': 10,
  'Q': 10,
  'K': 10,
  'A': (1, 11)
}
PLAYER_NAMES = ('John', 'Mark', 'Andrew', 'Steve', 'Andy', 'Jeremy', 'James')
MIN_PLAYER_COUNT = 0
MAX_PLAYER_COUNT = 6
TARGET = 21

PLAYER_DECISION = {
  'HIT': 'h',
  'STAND': 's',
  'DOUBLE_DOWN': 'dd',
  'SPLIT': 's'
}