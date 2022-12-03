import pygame


class Snake(pygame.sprite.Sprite):
  def __init__(self, NUM_OF_COL: int, NUM_OF_ROW: int, TILE_WIDTH: int, player: int):
    super().__init__()
    if player == 1:
      self.playerInput = self.player1Input
    else:
      self.playerInput = self.player2Input


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

  def update(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    self.drawSnake(TILE_WIDTH, TILE_HEIGHT, WINDOW)
    self.playerInput()    

  def drawSnake(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    snakeHeadRect = self.snakeHeadImg.get_rect(center = (self.headPosition[0] * TILE_WIDTH + 50 + TILE_WIDTH / 2, self.headPosition[1] * TILE_HEIGHT + 50  + TILE_HEIGHT / 2))
    WINDOW.blit(self.snakeHeadImg, snakeHeadRect)

    for tile in self.tailTab:
      #pygame.draw.rect(WINDOW, (0, 0, 255), pygame.Rect((tile[0] * TILE_WIDTH) + 50, (tile[1] * TILE_HEIGHT) + 50, TILE_WIDTH, TILE_HEIGHT ))
      self.imgVariant(TILE_WIDTH, TILE_HEIGHT, WINDOW)

  def drawTail(self, ckBefore, position, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
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

  def imgVariantDraw(self, ckBefore, ckAfter, position,  TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
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

  def imgVariant(self, TILE_WIDTH: int, TILE_HEIGHT: int, WINDOW):
    for index, tile in enumerate(self.tailTab):

      if index == 0:
        checkBefore = self.headPosition - self.tailTab[index]
        checkAfter = self.tailTab[index] - self.tailTab[index + 1]
        self.imgVariantDraw(checkBefore, checkAfter, tile, TILE_WIDTH, TILE_HEIGHT, WINDOW)

      elif index == len(self.tailTab) - 1:
        checkBefore = self.tailTab[index - 1] - self.tailTab[index]
        self.drawTail(checkBefore, tile, TILE_WIDTH, TILE_HEIGHT, WINDOW)
      
      else:
        checkBefore = self.tailTab[index - 1] - self.tailTab[index]
        checkAfter = self.tailTab[index] - self.tailTab[index + 1]
        self.imgVariantDraw(checkBefore, checkAfter, tile, TILE_WIDTH, TILE_HEIGHT, WINDOW)

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
