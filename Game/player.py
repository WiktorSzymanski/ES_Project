from typing import Tuple
import pygame


class Snake(pygame.sprite.Sprite):
  def __init__(self, start_pos: Tuple[int, int], TILE_WIDTH: int, player: int):
    super().__init__()
    if player == 1:
      self.player = 1
      self.color = (0, 0, 255)
      self.snakeHeadImg = pygame.image.load('./Game/graphics/blue_motor.png').convert_alpha()
    else:
      self.player = 2
      self.color = (255,255,0)
      self.snakeHeadImg = pygame.image.load('./Game/graphics/yellow_motor.png').convert_alpha()


    self.headPosition = start_pos
    self.tailTab = []
    self.ghost_mode = False

    self.ghost_mode_timer = 0

    self.endOfTailLastPosition = start_pos
    self.direction = 'up'
    self.newDirection = 'up'
    # self.snakeScale = (TILE_WIDTH / 40)
    self.snakeScale = 1/2


    self.snakeHeadImg = pygame.transform.rotozoom(self.snakeHeadImg, 0, self.snakeScale)
    self.snakeHeadImgTab = [self.snakeHeadImg, pygame.transform.rotate(self.snakeHeadImg, 270), pygame.transform.rotate(self.snakeHeadImg, 180), pygame.transform.rotate(self.snakeHeadImg, 90)]

  def update(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    self.drawSnake(TILE_WIDTH, TILE_HEIGHT, WINDOW)  

  def enterGhostMode(self):
    self.ghost_mode = True
    self.ghost_mode_timer = 10

  def drawSnake(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    snakeHeadRect = self.snakeHeadImg.get_rect(center = (self.headPosition[0] * TILE_WIDTH + 50 + TILE_WIDTH / 2, self.headPosition[1] * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(self.snakeHeadImg, snakeHeadRect)

  def move(self, gameArray):
    if not self.ghost_mode:
      gameArray[self.headPosition[0]][self.headPosition[1]] = self.player
    else:
      if self.ghost_mode_timer == 0:
        self.ghost_mode = False
      else:
        self.ghost_mode_timer -= 1

    if self.newDirection == 'left':
      self.headPosition = self.headPosition[0] - 1, self.headPosition[1]
      self.snakeHeadImg = self.snakeHeadImgTab[3]


    if self.newDirection == 'right':
      self.headPosition = self.headPosition[0] + 1, self.headPosition[1]
      self.snakeHeadImg = self.snakeHeadImgTab[1]


    if self.newDirection == 'up':
      self.headPosition = self.headPosition[0], self.headPosition[1] - 1
      self.snakeHeadImg = self.snakeHeadImgTab[0]


    if self.newDirection == 'down':
      self.headPosition = self.headPosition[0], self.headPosition[1] + 1
      self.snakeHeadImg = self.snakeHeadImgTab[2]


    self.direction = self.newDirection

  def grow(self):
    self.tailTab.append(self.endOfTailLastPosition)

  def playerInput(self, new_direction):
    if new_direction == 'up' and self.direction != 'down':
      self.newDirection = 'up'

    elif new_direction == 'down' and self.direction != 'up':
      self.newDirection = 'down'

    elif new_direction == 'left' and self.direction != 'right':
      self.newDirection = 'left'

    elif new_direction == 'right' and self.direction != 'left':
      self.newDirection = 'right'