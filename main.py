import pygame
import sys
import random

CAPTION = 'Snaaaaaaaake~'

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SNAKE_INIT_LENGTH = 10
SNAKE_INIT_WIDTH = 10
SNAKE_SPEED = 2

DIRECTIONS = {
    'UP': 1, 'DOWN': -1, 'LEFT': 2, 'RIGHT': -2
}


class Snake(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.first_x = random.randint(0, SCREEN_WIDTH)
        self.first_y = random.randint(0, SCREEN_HEIGHT)
        self.first_direction = random.choice(list(DIRECTIONS.keys()))
        self.speed = SNAKE_SPEED

        self.image = pygame.Surface((SNAKE_INIT_LENGTH, SNAKE_INIT_WIDTH))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

    def changeDirection(self, direction):
        if DIRECTIONS[self.direction] + DIRECTIONS[direction] != 0:
            self.direction = direction

    def update(self):
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed

        # 边界监测
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top < 20:
            self.rect.top = 20

    def reset(self):
        self.rect.x = self.first_x
        self.rect.y = self.first_y
        self.direction = self.first_direction


class Billboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.content = ''
        self.font = pygame.font.SysFont('consolas', 20)
        self.update()

    def rewrite(self, content):
        self.content = content

    def update(self):
        self.image = self.font.render(self.content, True, (255, 0, 0), BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    sprites = pygame.sprite.Group()
    snake = Snake()
    billboard = Billboard()
    sprites.add(snake)
    sprites.add(billboard)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.changeDirection('UP')
                    print('UP')
                if event.key == pygame.K_s:
                    snake.changeDirection('DOWN')
                    print('DOWN')
                if event.key == pygame.K_a:
                    snake.changeDirection('LEFT')
                    print('LEFT')
                if event.key == pygame.K_d:
                    snake.changeDirection('RIGHT')
                    print('RIGHT')

                if event.key == pygame.K_r:
                    snake.reset()
                    print('Reset')

        # Update
        slogan = 'Direction: {:5}, Position: ({:3}, {:3}, {:3}, {:3})'
        billboard.rewrite(slogan.format(snake.direction, snake.rect.top, snake.rect.bottom, snake.rect.left, snake.rect.right))
        sprites.update()

        # Draw / render
        screen.fill(BLACK)
        sprites.draw(screen)

        pygame.display.flip()
        clock.tick(SCREEN_FPS)


if __name__ == '__main__':
    main()
