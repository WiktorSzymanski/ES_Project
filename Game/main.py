from typing import List
from jinja2 import Undefined
import pygame
from sys import exit
from random import randint

from player import Snake
from game_logic import gameOverCondition, initGameArray


pygame.init()
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

WINTDOW_WIDTH = 700
WINDOW_HEIGHT = 700

PLAY_SURFACE_WIDTH = 600
PLAY_SURFACE_HEIGHT = 600

NUM_OF_COL = 60
NUM_OF_ROW = 60

TILE_WIDTH = PLAY_SURFACE_WIDTH / NUM_OF_COL
TILE_HEIGHT = PLAY_SURFACE_HEIGHT / NUM_OF_ROW

PLAY_SURFACE = pygame.Surface((PLAY_SURFACE_WIDTH,PLAY_SURFACE_HEIGHT))

CURRENT_SCORE = Undefined
gameArray = Undefined
who_won = Undefined


WINDOW = pygame.display.set_mode((WINTDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('TRON ARCADE')


def drawBackground():
  WINDOW.fill((100, 100, 100))

def drawLines():
  lineColor = (121, 144, 147)

  for i in range(1, NUM_OF_ROW):
    nextLinePositionY = (PLAY_SURFACE_HEIGHT/NUM_OF_ROW) * i
    pygame.draw.line(PLAY_SURFACE, lineColor, (0, nextLinePositionY), (PLAY_SURFACE_WIDTH, nextLinePositionY))

  for i in range(1, NUM_OF_COL):
    nextLinePositionX = (PLAY_SURFACE_HEIGHT/NUM_OF_COL) * i
    pygame.draw.line(PLAY_SURFACE, lineColor, (nextLinePositionX, 0), (nextLinePositionX, PLAY_SURFACE_HEIGHT))

def drawWalls():
  Color1 = (2, 247, 247)
  Color2 = (255, 255, 0)

  for rowIdx in range(NUM_OF_COL):
    for colIdx in range(NUM_OF_ROW):
      if gameArray[rowIdx][colIdx] == 1:
        color = Color1
      elif gameArray[rowIdx][colIdx] == 2:
        color = Color2
      else:
        color = (0, 0, 0)
      
      pygame.draw.rect(PLAY_SURFACE, color, pygame.Rect( (rowIdx * TILE_WIDTH), (colIdx * TILE_HEIGHT), TILE_WIDTH, TILE_HEIGHT ))
  
def drawPlaySurface():
  # drawLines()
  WINDOW.blit(PLAY_SURFACE, (50, 50))

def printScore():
  scoreTxt = font.render(f'Score: {CURRENT_SCORE}', True, (0,0,0))
  scoreRect = scoreTxt.get_rect(center = (WINTDOW_WIDTH / 2, 25))
  WINDOW.blit(scoreTxt, scoreRect)


gameActive = False

SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 50)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if event.type == SNAKE_MOVE and gameActive:
      snake.move(gameArray)
      snake2.move(gameArray)

  if gameActive:
    drawBackground()
    printScore()
    drawPlaySurface()
    drawWalls()

    gameActive, who_won = gameOverCondition([snake, snake2], NUM_OF_ROW, NUM_OF_COL, gameArray)

    snake.update(TILE_WIDTH, TILE_HEIGHT, WINDOW)
    snake2.update(TILE_WIDTH, TILE_HEIGHT, WINDOW)
  else:
    WINDOW.fill((121, 144, 147))

    nameTxt = font.render('TRON ARCADE', True, (0, 0, 0))
    nameRect = nameTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
    WINDOW.blit(nameTxt, nameRect)

    startTxt = font.render('Press Enter to start', True, (0, 0, 0))
    startRect = startTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100))
    WINDOW.blit(startTxt, startRect)

    if who_won != Undefined:
      if who_won != 0:
        overScoreTxt = font.render(f'Player {who_won} won!', True, (0, 0, 0))
      else:
        overScoreTxt = font.render(f'Draw!', True, (0, 0, 0))

      overScoreRect = overScoreTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2))
      WINDOW.blit(overScoreTxt, overScoreRect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
      gameActive = True
      snake = Snake((NUM_OF_COL-5, NUM_OF_ROW-5), TILE_WIDTH, 1)
      snake2 = Snake((4, 4), TILE_WIDTH, 2)
      snake2.newDirection = 'down'
      gameArray = initGameArray(NUM_OF_ROW, NUM_OF_COL)

      CURRENT_SCORE = 0

  pygame.display.update()
  clock.tick(60)