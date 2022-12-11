from typing import Tuple
import pygame


class Snake(pygame.sprite.Sprite):
  def __init__(self, start_pos: Tuple[int, int], TILE_WIDTH: int, player: int):
    super().__init__()
    if player == 1:
      self.playerInput = self.player1Input
      self.color = (0, 0, 255)
    else:
      self.playerInput = self.player2Input
      self.color = (255,255,0)


    self.headPosition = pygame.Vector2(start_pos)
    self.tailTab = []

    self.endOfTailLastPosition = pygame.Vector2(start_pos)
    self.direction = 'up'
    self.newDirection = 'up'
    self.snakeScale = (TILE_WIDTH / 40)

    self.snakeHeadImg = pygame.image.load('./graphics/head.png').convert_alpha()
    self.snakeHeadImg = pygame.transform.rotozoom(self.snakeHeadImg, 0, self.snakeScale)
    self.snakeHeadImgTab = [self.snakeHeadImg, pygame.transform.rotate(self.snakeHeadImg, 270), pygame.transform.rotate(self.snakeHeadImg, 180), pygame.transform.rotate(self.snakeHeadImg, 90)]

  def update(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    self.drawSnake(TILE_WIDTH, TILE_HEIGHT, WINDOW)
    self.playerInput()    

  def drawSnake(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    snakeHeadRect = self.snakeHeadImg.get_rect(center = (self.headPosition[0] * TILE_WIDTH + 50 + TILE_WIDTH / 2, self.headPosition[1] * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(self.snakeHeadImg, snakeHeadRect)

    for tile in self.tailTab:
      pygame.draw.rect(WINDOW, self.color, pygame.Rect((tile[0] * TILE_WIDTH) + 50, (tile[1] * TILE_HEIGHT) + 50, TILE_WIDTH, TILE_HEIGHT ))

  def move(self):
    self.tailTab.insert(0,self.headPosition)

    if self.newDirection == 'left':
      self.headPosition = pygame.Vector2(self.headPosition[0] - 1, self.headPosition[1])
      self.snakeHeadImg = self.snakeHeadImgTab[3]


    if self.newDirection == 'right':
      self.headPosition = pygame.Vector2(self.headPosition[0] + 1, self.headPosition[1])
      self.snakeHeadImg = self.snakeHeadImgTab[1]


    if self.newDirection == 'up':
      self.headPosition = pygame.Vector2(self.headPosition[0], self.headPosition[1] - 1)
      self.snakeHeadImg = self.snakeHeadImgTab[0]


    if self.newDirection == 'down':
      self.headPosition = pygame.Vector2(self.headPosition[0], self.headPosition[1] + 1)
      self.snakeHeadImg = self.snakeHeadImgTab[2]


    self.direction = self.newDirection

  def grow(self):
    self.tailTab.append(self.endOfTailLastPosition)

  def playerInput(self):
    pass

  def player1Input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and self.direction != 'down':
      self.newDirection = 'up'

    elif keys[pygame.K_DOWN] and self.direction != 'up':
      self.newDirection = 'down'

    elif keys[pygame.K_LEFT] and self.direction != 'right':
      self.newDirection = 'left'

    elif keys[pygame.K_RIGHT] and self.direction != 'left':
      self.newDirection = 'right'

  def player2Input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and self.direction != 'down':
      self.newDirection = 'up'

    elif keys[pygame.K_s] and self.direction != 'up':
      self.newDirection = 'down'

    elif keys[pygame.K_a] and self.direction != 'right':
      self.newDirection = 'left'

    elif keys[pygame.K_d] and self.direction != 'left':
      self.newDirection = 'right'
