from glob import glob
from re import A
import pygame
from sys import exit
from random import randint

class Snake(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.length = 3
    self.headPosition = (10, 10)
    self.tailTab = [(10,11),(10,12)]
    self.endOfTailLastPosition = (10,12)
    self.direction = 'up'

  def update(self):
    self.playerInput()
    self.move()

  def move(self):
    self.tailTab.insert(0,self.headPosition)
    self.endOfTailLastPosition = self.tailTab.pop()

    if self.direction == 'left':
      self.headPosition = (self.headPosition[0] - 1, self.headPosition[1])
    
    if self.direction == 'right':
      self.headPosition = (self.headPosition[0] + 1, self.headPosition[1])
    
    if self.direction == 'up':
      self.headPosition = (self.headPosition[0], self.headPosition[1] - 1)
    
    if self.direction == 'down':
      self.headPosition = (self.headPosition[0], self.headPosition[1] + 1)

  def grow(self):
    self.tailTab.append(self.endOfTailLastPosition)

  def playerInput(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and self.direction != 'down':
      self.direction = 'up'

    if keys[pygame.K_DOWN] and self.direction != 'up':
      self.direction = 'down'

    if keys[pygame.K_LEFT] and self.direction != 'right':
      self.direction = 'left'

    if keys[pygame.K_RIGHT] and self.direction != 'left':
      self.direction = 'right'

class Apple(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.position = (5,5)
    self.isEatten = False
  
  def update(self):
    if self.isEatten:
      self.spawn()

  def spawn(self):
    x = randint(0, NUM_OF_COL-1)
    y = randint(0, NUM_OF_COL-1)

    self.position = (x,y)
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

CURRENT_SCORE = 0

GAME_MATRIX = []
for _ in range(NUM_OF_COL + 1):
    row = []
    for _ in range(NUM_OF_ROW + 1):
      row.append(0)
    GAME_MATRIX.append(row)


WINDOW = pygame.display.set_mode((WINTDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('py-snake')

def clearGameMatrix():
  for i in range(NUM_OF_COL):
    for j in range(NUM_OF_ROW):
      GAME_MATRIX[i][j] = 0

def drawBackground():
  WINDOW.fill((121, 144, 147))

def drawLines(playSurface ,numOfCol, numOfRow):
  lineColor = (121, 144, 147)

  for i in range(1, numOfRow):
    nextLinePositionY = (PLAY_SURFACE_HEIGHT/numOfRow) * i
    pygame.draw.line(playSurface, lineColor, (0, nextLinePositionY), (PLAY_SURFACE_WIDTH, nextLinePositionY))

  for i in range(1, numOfCol):
    nextLinePositionX = (PLAY_SURFACE_HEIGHT/numOfCol) * i
    pygame.draw.line(playSurface, lineColor, (nextLinePositionX, 0), (nextLinePositionX, PLAY_SURFACE_HEIGHT))

def drawTilesAndSnake(playSurface, numOfCol, numOfRow):
  tileWidth = PLAY_SURFACE_WIDTH / numOfCol
  tileHeight = PLAY_SURFACE_HEIGHT / numOfRow

  tileColor1 = (16, 148, 114)
  tileColor2 = (121, 175, 147)
  appleColor = (255, 0, 0)
  snakeColor = (0, 0, 255)

  for rowIdx in range(len(GAME_MATRIX)):
    for colIdx in range(len(GAME_MATRIX[rowIdx])):
      if (rowIdx + colIdx) % 2 == 0:
        color = tileColor1
      else:
        color = tileColor2

      if GAME_MATRIX[rowIdx][colIdx] == 1:
        color = snakeColor


      if GAME_MATRIX[rowIdx][colIdx] == 2:
        color = appleColor
      
      pygame.draw.rect(playSurface, color, pygame.Rect( (rowIdx * tileWidth), (colIdx * tileHeight), tileWidth, tileHeight ))

def addSnakeToMatrix(snake):
  GAME_MATRIX[snake.headPosition[0]][snake.headPosition[1]] = 1

  for tile in snake.tailTab:
    GAME_MATRIX[tile[0]][tile[1]] = 1
  
def addAppleToMatrix(apple):
  GAME_MATRIX[apple.position[0]][apple.position[1]] = 2

def drawPlaySurface(numOfCol, numOfRow, snake, apple):
  clearGameMatrix()
  addAppleToMatrix(apple)
  addSnakeToMatrix(snake)

  playSurface = pygame.Surface((PLAY_SURFACE_WIDTH,PLAY_SURFACE_HEIGHT))

  # drawLines(playSurface, numOfCol, numOfRow)
  drawTilesAndSnake(playSurface, numOfCol, numOfRow)

  WINDOW.blit(playSurface, (50, 50))

def gameOverCondition(snake):
  if (snake.headPosition[0] <= -1 or
      snake.headPosition[1] <= -1 or
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
    CURRENT_SCORE += 1
    print('apple Eatten')

def printScore():
  scoreTxt = font.render(f'Score: {CURRENT_SCORE}', True, (0,0,0))
  WINDOW.blit(scoreTxt, (WINTDOW_WIDTH/2 - 10, 1))

snake = Snake()
apple = Apple()

gameActive = True

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()


  if gameActive:
    drawBackground()
    printScore()
    drawPlaySurface(NUM_OF_COL, NUM_OF_ROW, snake, apple)
    eatManager(snake, apple)

    gameActive = gameOverCondition(snake)

    snake.update()
    apple.update()
    print(snake.headPosition)
  else:
    WINDOW.fill((121, 144, 147))
    gameOverTxt = font.render('Game Over', True, (255, 0, 0))
    WINDOW.blit(gameOverTxt, (10,10))

  pygame.display.update()
  clock.tick(10)