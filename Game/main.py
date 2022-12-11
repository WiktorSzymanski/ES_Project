from jinja2 import Undefined
import pygame
from sys import exit
from random import randint

class Snake(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.headPosition = pygame.Vector2(NUM_OF_COL//2, NUM_OF_ROW//2)
    self.tailTab = [pygame.Vector2(NUM_OF_COL//2, NUM_OF_ROW//2 + 1),pygame.Vector2(NUM_OF_COL//2, NUM_OF_ROW//2 + 2)]

    self.endOfTailLastPosition = pygame.Vector2(NUM_OF_COL//2, NUM_OF_ROW//2)
    self.direction = 'up'
    self.newDirection = 'up'
    self.snakeScale = (TILE_WIDTH / 40)

    self.snakeHeadImg = pygame.image.load('./graphics/head.png').convert_alpha()
    self.snakeHeadImg = pygame.transform.rotozoom(self.snakeHeadImg, 0, self.snakeScale)
    self.snakeHeadImgTab = [self.snakeHeadImg, pygame.transform.rotate(self.snakeHeadImg, 270), pygame.transform.rotate(self.snakeHeadImg, 180), pygame.transform.rotate(self.snakeHeadImg, 90)]

    self.snakeBodyImg = pygame.image.load('./graphics/body.png').convert_alpha()
    self.snakeBodyImg = pygame.transform.rotozoom(self.snakeBodyImg, 0, self.snakeScale)
    self.snakeBodyImgTab = [self.snakeBodyImg, pygame.transform.rotate(self.snakeBodyImg, 270), pygame.transform.rotate(self.snakeBodyImg, 180), pygame.transform.rotate(self.snakeBodyImg, 90)]

    self.snakeTurnLeftImg = pygame.image.load('./graphics/turn.png').convert_alpha()
    self.snakeTurnLeftImg = pygame.transform.rotozoom(self.snakeTurnLeftImg, 0, self.snakeScale)
    self.snakeTurnLeftImgTab = [self.snakeTurnLeftImg, pygame.transform.rotate(self.snakeTurnLeftImg, 270), pygame.transform.rotate(self.snakeTurnLeftImg, 180), pygame.transform.rotate(self.snakeTurnLeftImg, 90)]

    self.snakeTurnRightImgTab = [pygame.transform.flip(self.snakeTurnLeftImgTab[0], False, True), pygame.transform.flip(self.snakeTurnLeftImgTab[1], False, True), pygame.transform.flip(self.snakeTurnLeftImgTab[2], False, True), pygame.transform.flip(self.snakeTurnLeftImgTab[3], False, True)]

    self.snakeTailImg = pygame.image.load('./graphics/tail.png').convert_alpha()
    self.snakeTailImg = pygame.transform.rotozoom(self.snakeTailImg, 0, self.snakeScale)
    self.snakeTailImgTab = [self.snakeTailImg, pygame.transform.rotate(self.snakeTailImg, 270), pygame.transform.rotate(self.snakeTailImg, 180), pygame.transform.rotate(self.snakeTailImg, 90)]

  def update(self):
    self.drawSnake()
    self.playerInput()    

  def drawSnake(self):
    snakeHeadRect = self.snakeHeadImg.get_rect(center = (self.headPosition[0] * TILE_WIDTH + 50 + TILE_WIDTH / 2, self.headPosition[1] * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(self.snakeHeadImg, snakeHeadRect)

    for tile in self.tailTab:
      #pygame.draw.rect(WINDOW, (0, 0, 255), pygame.Rect((tile[0] * TILE_WIDTH) + 50, (tile[1] * TILE_HEIGHT) + 50, TILE_WIDTH, TILE_HEIGHT ))
      self.imgVariant()

  def drawTail(self, ckBefore, position):
    if (ckBefore == (1, 0)):
      img = self.snakeTailImgTab[1]
    elif (ckBefore == (-1, 0)):
      img = self.snakeTailImgTab[3]
    elif (ckBefore == (0, 1)):
      img = self.snakeTailImgTab[2]
    elif (ckBefore == (0, -1)):
      img = self.snakeTailImgTab[0]

    snakeBodyRect = img.get_rect(center = (position.x * TILE_WIDTH + 50 + TILE_WIDTH / 2, position.y * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(img, snakeBodyRect)

  def imgVariantDraw(self, ckBefore, ckAfter, position):
    if (ckBefore == ckAfter == (-1, 0)):
      img = self.snakeBodyImgTab[1]
    elif (ckBefore == ckAfter == (1, 0)):
      img = self.snakeBodyImgTab[3]
    elif (ckBefore == ckAfter == (0, -1)):
      img = self.snakeBodyImgTab[2]
    elif (ckBefore == ckAfter == (0, 1)):
      img = self.snakeBodyImgTab[0]
    elif (ckBefore == (-1, 0) and ckAfter == (0, -1)):
      img = self.snakeTurnLeftImgTab[0]
    elif (ckBefore == (0, -1) and ckAfter == (1, 0)):
      img = self.snakeTurnLeftImgTab[1]
    elif (ckBefore == (1, 0) and ckAfter == (0, 1)):
      img = self.snakeTurnLeftImgTab[2]
    elif (ckBefore == (0, 1) and ckAfter == (-1, 0)):
      img = self.snakeTurnLeftImgTab[3]
    # Right
    elif (ckBefore == (0, -1) and ckAfter == (-1, 0)):
      img = self.snakeTurnRightImgTab[3]
    elif (ckBefore == (1, 0) and ckAfter == (0, -1)):
      img = self.snakeTurnRightImgTab[2]
    elif (ckBefore == (0, 1) and ckAfter == (1, 0)):
      img = self.snakeTurnRightImgTab[1]
    elif (ckBefore == (-1, 0) and ckAfter == (0, 1)):
      img = self.snakeTurnRightImgTab[0]
    else:
      img = self.snakeTailImg

    snakeBodyRect = img.get_rect(center = (position.x * TILE_WIDTH + 50 + TILE_WIDTH / 2, position.y * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(img, snakeBodyRect)



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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and self.direction != 'down':
      self.newDirection = 'up'

    elif keys[pygame.K_DOWN] and self.direction != 'up':
      self.newDirection = 'down'

    elif keys[pygame.K_LEFT] and self.direction != 'right':
      self.newDirection = 'left'

    elif keys[pygame.K_RIGHT] and self.direction != 'left':
      self.newDirection = 'right'
      
class Apple(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.position = pygame.Vector2(1, 1)
    self.isEatten = True
    self.appleImg = pygame.image.load('./graphics/apple.png').convert_alpha()
  
  def update(self, snakeHead, snakeTail):
    self.drawApple()
    if self.isEatten:
      self.spawn(snakeHead, snakeTail)

  def drawApple(self):
    appleRect = self.appleImg.get_rect(center = (self.position[0] * TILE_WIDTH + 50 + TILE_WIDTH / 2, self.position[1] * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(self.appleImg, appleRect)

  def spawn(self, snakeHead, snakeTail):
    self.position = snakeHead

    while self.position in snakeTail or self.position == snakeHead:
      x = randint(0, NUM_OF_COL-1)
      y = randint(0, NUM_OF_COL-1)
      self.position = pygame.Vector2(x,y)

    self.isEatten = False


pygame.init()
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

WINTDOW_WIDTH = 700
WINDOW_HEIGHT = 700

PLAY_SURFACE_WIDTH = 600
PLAY_SURFACE_HEIGHT = 600

NUM_OF_COL = 20
NUM_OF_ROW = 20

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

def gameOverCondition(snake):
  if (snake.headPosition[0] < 0 or
      snake.headPosition[1] < 0 or
      snake.headPosition[0] >= NUM_OF_ROW or
      snake.headPosition[1] >= NUM_OF_COL or
      snake.headPosition in snake.tailTab):
    return False
  return True

def eatManager(snake, apple):
  global CURRENT_SCORE

  if snake.headPosition == apple.position:
    apple.isEatten = True
    snake.grow()
    CURRENT_SCORE += 100

def printScore():
  scoreTxt = font.render(f'Score: {CURRENT_SCORE}', True, (0,0,0))
  scoreRect = scoreTxt.get_rect(center = (WINTDOW_WIDTH / 2, 25))
  WINDOW.blit(scoreTxt, scoreRect)

snake = Snake()
apple = Apple()

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

  if gameActive:
    drawBackground()
    printScore()
    drawPlaySurface()
    eatManager(snake, apple)

    gameActive = gameOverCondition(snake)

    snake.update()
    apple.update(snake.headPosition, snake.tailTab)
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
      snake = Snake()
      apple = Apple()
      CURRENT_SCORE = 0

  pygame.display.update()
  clock.tick(60)