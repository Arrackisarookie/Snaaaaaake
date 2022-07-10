import pygame
import sys
import random

CAPTION = 'Snaaaaaaaake~'
WIDTH = 640
HEIGHT = 480
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPEED = 1


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.first_x = random.random() * WIDTH
        self.first_y = random.random() * HEIGHT
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

        self.speed_x = 0
        self.speed_y = 0

    def control(self, x, y):
        self.speed_x += x
        self.speed_y += y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 边界监测
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < 20:
            self.rect.top = 20

    def reset(self):
        self.rect.x = self.first_x
        self.rect.y = self.first_y


class SpeedLabel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.content = 'speed: , position:'
        self.font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 20)
        self.image = self.font.render(self.content, True, (255, 0, 0), BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-30, 10)

    def updateLabel(self, speed, position):
        self.content = 'speed: {}, position: {}'.format(speed, position)
        self.image = self.font.render(self.content, True, (255, 0, 0), BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
snake = Snake()
speedLabel = SpeedLabel()
sprites.add(snake)
sprites.add(speedLabel)


info = 'speed_xy: ({}, {})'
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 油门
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.control(0, -SPEED)
                print('UP')
            if event.key == pygame.K_a:
                snake.control(-SPEED, 0)
                print('LEFT')
            if event.key == pygame.K_s:
                snake.control(0, SPEED)
                print('DOWN')
            if event.key == pygame.K_d:
                snake.control(SPEED, 0)
                print('RIGHT')

            if event.key == pygame.K_r:
                snake.reset()
                print('Reset')

        # 刹车
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                snake.control(0, -SPEED)
                print('UP STOP')
            if event.key == pygame.K_a:
                snake.control(-SPEED, 0)
                print('LEFT STOP')
            if event.key == pygame.K_s:
                snake.control(0, SPEED)
                print('DOWN STOP')
            if event.key == pygame.K_d:
                snake.control(SPEED, 0)
                print('RIGHT STOP')

    # Update
    speedLabel.updateLabel((snake.speed_x, snake.speed_y), (snake.rect.top, snake.rect.bottom, snake.rect.left, snake.rect.right))
    sprites.update()

    # Draw / render
    screen.fill(BLACK)
    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
