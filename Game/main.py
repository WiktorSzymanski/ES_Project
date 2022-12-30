from typing import List
from jinja2 import Undefined
import pygame
from sys import exit
from random import randint

from multiprocessing import Queue


from Game.player import Snake
from Game.game_logic import gameOverCondition, initGameArray

class Game:
  def __init__(self) -> None:
    pygame.init()
    self.clock = pygame.time.Clock()

    self.font = pygame.font.Font(None, 50)

    self.WINTDOW_WIDTH = 700
    self.WINDOW_HEIGHT = 700

    self.PLAY_SURFACE_WIDTH = 600
    self.PLAY_SURFACE_HEIGHT = 600

    self.NUM_OF_COL = 60
    self.NUM_OF_ROW = 60

    self.TILE_WIDTH = self.PLAY_SURFACE_WIDTH / self.NUM_OF_COL
    self.TILE_HEIGHT = self.PLAY_SURFACE_HEIGHT / self.NUM_OF_ROW

    self.PLAY_SURFACE = pygame.Surface((self.PLAY_SURFACE_WIDTH,self.PLAY_SURFACE_HEIGHT))

    self.CURRENT_SCORE = Undefined
    self.gameArray = Undefined
    self.who_won = Undefined
    self.players = Undefined

    self.readyCheck = [False, False]


    self.WINDOW = pygame.display.set_mode((self.WINTDOW_WIDTH,self.WINDOW_HEIGHT))
    pygame.display.set_caption('TRON ARCADE')

    self.gameActive = False

    self.SNAKE_MOVE = pygame.USEREVENT
    pygame.time.set_timer(self.SNAKE_MOVE, 250)

  def readInput(self, player: int, direction: str):
    self.players[player-1].newDirection = direction

  def drawBackground(self):
    self.WINDOW.fill((100, 100, 100))

  def drawLines(self):
    lineColor = (121, 144, 147)

    for i in range(1, self.NUM_OF_ROW):
      nextLinePositionY = (self.PLAY_SURFACE_HEIGHT/self.NUM_OF_ROW) * i
      pygame.draw.line(self.PLAY_SURFACE, lineColor, (0, nextLinePositionY), (self.PLAY_SURFACE_WIDTH, nextLinePositionY))

    for i in range(1, self.NUM_OF_COL):
      nextLinePositionX = (self.PLAY_SURFACE_HEIGHT/self.NUM_OF_COL) * i
      pygame.draw.line(self.PLAY_SURFACE, lineColor, (nextLinePositionX, 0), (nextLinePositionX, self.PLAY_SURFACE_HEIGHT))

  def drawWalls(self):
    Color1 = (2, 247, 247)
    Color2 = (255, 255, 0)

    for rowIdx in range(self.NUM_OF_COL):
      for colIdx in range(self.NUM_OF_ROW):
        if self.gameArray[rowIdx][colIdx] == 1:
          color = Color1
        elif self.gameArray[rowIdx][colIdx] == 2:
          color = Color2
        else:
          color = (0, 0, 0)
        
        pygame.draw.rect(self.PLAY_SURFACE, color, pygame.Rect( (rowIdx * self.TILE_WIDTH), (colIdx * self.TILE_HEIGHT), self.TILE_WIDTH, self.TILE_HEIGHT ))
    
  def drawPlaySurface(self):
    # drawLines()
    self.WINDOW.blit(self.PLAY_SURFACE, (50, 50))

  def printScore(self):
    scoreTxt = self.font.render(f'Score: {self.CURRENT_SCORE}', True, (0,0,0))
    scoreRect = scoreTxt.get_rect(center = (self.WINTDOW_WIDTH / 2, 25))
    self.WINDOW.blit(scoreTxt, scoreRect)

  def startGame(self):
    self.gameActive = True
    self.players = [Snake((self.NUM_OF_COL-5, self.NUM_OF_ROW-5), self.TILE_WIDTH, 1), Snake((4, 4), self.TILE_WIDTH, 2)]
    self.players[1].newDirection = 'down'
    self.gameArray = initGameArray(self.NUM_OF_ROW, self.NUM_OF_COL)

  def run(self, queue):
  

    while True:
      while not queue.empty():
        command = queue.get()
        if command[1] == 'start':
          self.readyCheck[command[0] - 1] = True
        elif self.gameActive:
          if command[1] == 'ghost':
            if self.players[command[0] - 1].cooldown == 0:
              self.players[command[0] - 1].enterGhostMode()
          else:
            self.players[command[0] - 1].playerInput(command[1])

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

        if event.type == self.SNAKE_MOVE and self.gameActive:
          self.players[0].move(self.gameArray)
          self.players[1].move(self.gameArray)

      if self.gameActive:
        self.drawBackground()
        # self.printScore()
        self.drawPlaySurface()
        self.drawWalls()

        self.gameActive, self.who_won = gameOverCondition(self.players, self.NUM_OF_ROW, self.NUM_OF_COL, self.gameArray)

        self.players[0].update(self.TILE_WIDTH, self.TILE_HEIGHT, self.WINDOW)
        self.players[1].update(self.TILE_WIDTH, self.TILE_HEIGHT, self.WINDOW)

        if not self.gameActive:
          self.readyCheck = [False, False]
      else:
        if self.readyCheck[0] and self.readyCheck[1]:
          self.startGame()
        self.WINDOW.fill((121, 144, 147))

        self.nameTxt = self.font.render('TRON ARCADE', True, (0, 0, 0))
        self.nameRect = self.nameTxt.get_rect(center = (self.WINTDOW_WIDTH/2, self.WINDOW_HEIGHT/2 - 100))
        self.WINDOW.blit(self.nameTxt, self.nameRect)

        self.player1 = self.font.render(f'Player1 {self.readyCheck[0]}', True, (0, 0, 0))
        self.player2 = self.font.render(f'Player2 {self.readyCheck[1]}', True, (0, 0, 0))
        self.startRect = self.player1.get_rect(center = (self.WINTDOW_WIDTH/2, self.WINDOW_HEIGHT/2 + 100))
        self.startRect2 = self.player2.get_rect(center = (self.WINTDOW_WIDTH/2, self.WINDOW_HEIGHT/2 + 150))
        self.WINDOW.blit(self.player1, self.startRect)
        self.WINDOW.blit(self.player2, self.startRect2)

        if self.who_won != Undefined:
          if self.who_won != 0:
            self.overScoreTxt = self.font.render(f'Player {self.who_won} won!', True, (0, 0, 0))
          else:
            self.overScoreTxt = self.font.render(f'Draw!', True, (0, 0, 0))

          self.overScoreRect = self.overScoreTxt.get_rect(center = (self.WINTDOW_WIDTH/2, self.WINDOW_HEIGHT/2))
          self.WINDOW.blit(self.overScoreTxt, self.overScoreRect)

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_RETURN]:
          self.startGame()

          self.CURRENT_SCORE = 0

      pygame.display.update()
      self.clock.tick(60)

if __name__ == '__main__':
  game = Game()

  game.run()