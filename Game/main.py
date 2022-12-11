from typing import List
from jinja2 import Undefined
import pygame
from sys import exit
from random import randint

from player import Snake
from game_logic import gameOverCondition, initGameArray, placePlayersOnStartPositions


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



WINDOW = pygame.display.set_mode((WINTDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('py-snake')


def drawBackground():
  WINDOW.fill((121, 144, 147))

def drawLines():
  lineColor = (121, 144, 147)

  for i in range(1, NUM_OF_ROW):
    nextLinePositionY = (PLAY_SURFACE_HEIGHT/NUM_OF_ROW) * i
    pygame.draw.line(PLAY_SURFACE, lineColor, (0, nextLinePositionY), (PLAY_SURFACE_WIDTH, nextLinePositionY))

  for i in range(1, NUM_OF_COL):
    nextLinePositionX = (PLAY_SURFACE_HEIGHT/NUM_OF_COL) * i
    pygame.draw.line(PLAY_SURFACE, lineColor, (nextLinePositionX, 0), (nextLinePositionX, PLAY_SURFACE_HEIGHT))

def drawTiles():
  tileColor1 = (111, 165, 137)
  tileColor2 = (121, 175, 147)

  for rowIdx in range(NUM_OF_COL):
    for colIdx in range(NUM_OF_ROW):
      if (rowIdx + colIdx) % 2 == 0:
        color = tileColor1
      else:
        color = tileColor2
      
      pygame.draw.rect(PLAY_SURFACE, color, pygame.Rect( (rowIdx * TILE_WIDTH), (colIdx * TILE_HEIGHT), TILE_WIDTH, TILE_HEIGHT ))
  
def drawPlaySurface():
  # drawLines()
  drawTiles()

  WINDOW.blit(PLAY_SURFACE, (50, 50))

def printScore():
  scoreTxt = font.render(f'Score: {CURRENT_SCORE}', True, (0,0,0))
  scoreRect = scoreTxt.get_rect(center = (WINTDOW_WIDTH / 2, 25))
  WINDOW.blit(scoreTxt, scoreRect)


gameActive = False

SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 100)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if event.type == SNAKE_MOVE and gameActive:
      snake.move()
      snake2.move()

  if gameActive:
    drawBackground()
    printScore()
    drawPlaySurface()

    gameActive = gameOverCondition([snake, snake2], NUM_OF_ROW, NUM_OF_COL)

    snake.update(TILE_WIDTH, TILE_HEIGHT, WINDOW)
    snake2.update(TILE_WIDTH, TILE_HEIGHT, WINDOW)
  else:
    WINDOW.fill((121, 144, 147))

    nameTxt = font.render('py-snake', True, (0, 0, 0))
    nameRect = nameTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
    WINDOW.blit(nameTxt, nameRect)

    startTxt = font.render('Press Enter to start', True, (0, 0, 0))
    startRect = startTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100))
    WINDOW.blit(startTxt, startRect)

    if CURRENT_SCORE != Undefined:
      overScoreTxt = font.render(f'Your score: {CURRENT_SCORE}', True, (0, 0, 0))
      overScoreRect = overScoreTxt.get_rect(center = (WINTDOW_WIDTH/2, WINDOW_HEIGHT/2))
      WINDOW.blit(overScoreTxt, overScoreRect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
      gameActive = True
      snake = Snake((NUM_OF_COL-5, NUM_OF_ROW-5), TILE_WIDTH, 1)
      snake2 = Snake((5, 5), TILE_WIDTH, 2)
      snake2.newDirection = 'down'
      gameArray = initGameArray(NUM_OF_ROW, NUM_OF_COL)
      placePlayersOnStartPositions(gameArray, NUM_OF_ROW, NUM_OF_COL)

      CURRENT_SCORE = 0

  pygame.display.update()
  clock.tick(60)