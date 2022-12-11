from typing import List
import pygame

from player import Snake


def initGameArray(row_num, col_num) -> List[List[int]]:
  return [[0]*row_num for _ in range(col_num)]


def placePlayersOnStartPositions(gameArray: List[List[int]], row_num: int, col_num: int) -> None:
  gameArray[row_num - 5][col_num - 5] = 1
  gameArray[5][5] = 2


def gameOverCondition(players: List[Snake], NUM_OF_ROW, NUM_OF_COL):
  for snake in players:
    if (snake.headPosition[0] < 0 or
        snake.headPosition[1] < 0 or
        snake.headPosition[0] >= NUM_OF_ROW or
        snake.headPosition[1] >= NUM_OF_COL):
      return False
    for tail in players:
      if (snake.headPosition in tail.tailTab):
        return False
  return True