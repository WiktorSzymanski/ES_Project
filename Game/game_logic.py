from typing import List
from jinja2 import Undefined

from Game.player import Snake


def initGameArray(row_num, col_num) -> List[List[int]]:
  return [[0]*row_num for _ in range(col_num)]


def gameOverCondition(players: List[Snake], NUM_OF_ROW, NUM_OF_COL, gameArray):
  continue_game = True
  who_lost = 0

  for snake in players:
    if (snake.headPosition[0] < 0 or
        snake.headPosition[1] < 0 or
        snake.headPosition[0] >= NUM_OF_ROW or
        snake.headPosition[1] >= NUM_OF_COL or
        gameArray[snake.headPosition[0]][snake.headPosition[1]] != 0):
      continue_game = False
      if who_lost != 0:
        who_lost = 3
      else:
        who_lost = snake.player
  

  return continue_game, 3 - who_lost