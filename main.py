import pygame
import sys
import random

CAPTION = 'Snaaaaaaaake~'

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

FOOD_SIZE = 15
SNAKE_INIT_LENGTH = 15
SNAKE_INIT_WIDTH = 15
SNAKE_SPEED = 5

DIRECTIONS = {
    'UP': 1, 'DOWN': -1, 'LEFT': 2, 'RIGHT': -2
}


class Food(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((FOOD_SIZE, FOOD_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.reborn()

    def reborn(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE)


class Snake(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.first_x = random.randint(0, SCREEN_WIDTH - SNAKE_INIT_WIDTH)
        self.first_y = random.randint(0, SCREEN_HEIGHT - SNAKE_INIT_LENGTH)
        self.first_direction = random.choice(list(DIRECTIONS.keys()))
        self.speed = SNAKE_SPEED
        self.score = 0

        self.image = pygame.Surface((SNAKE_INIT_LENGTH, SNAKE_INIT_WIDTH))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

    def hit(self):
        self.score += 1

    def change_direction(self, direction):
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
        elif self.rect.top < 0:
            self.rect.top = 0

    def reset(self):
        self.rect.x = self.first_x
        self.rect.y = self.first_y
        self.direction = self.first_direction


class Billboard(pygame.sprite.Sprite):
    def __init__(self, template, left=0, top=0):
        pygame.sprite.Sprite.__init__(self)
        self.template = template
        self.left = left
        self.top = top
        self.content = ''
        self.font = pygame.font.SysFont('consolas', 20)
        self.update()

    def rewrite(self, *args):
        self.content = self.template.format(*args)

    def update(self):
        self.image = self.font.render(self.content, True, (255, 0, 0), BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.left
        self.rect.y = self.top


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    sprites = pygame.sprite.Group()
    snake = Snake()
    direction_board = Billboard('Direction: {:5}', 0, 0)
    position_board = Billboard('Position: ({:3}, {:3}, {:3}, {:3})', 0, 20)
    score_board = Billboard('Score: {:3}', 0, 40)
    food = Food()
    sprites.add(direction_board)
    sprites.add(position_board)
    sprites.add(score_board)
    sprites.add(food)
    sprites.add(snake)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.change_direction('UP')
                    print('UP')
                if event.key == pygame.K_s:
                    snake.change_direction('DOWN')
                    print('DOWN')
                if event.key == pygame.K_a:
                    snake.change_direction('LEFT')
                    print('LEFT')
                if event.key == pygame.K_d:
                    snake.change_direction('RIGHT')
                    print('RIGHT')

                if event.key == pygame.K_r:
                    snake.reset()
                    print('Reset')

        if pygame.sprite.collide_rect(snake, food):
            snake.hit()
            food.reborn()

        # Update

        score_board.rewrite(snake.score)
        direction_board.rewrite(snake.direction)
        position_board.rewrite(snake.rect.top, snake.rect.bottom, snake.rect.left, snake.rect.right)
        sprites.update()

        # Draw / render
        screen.fill(BLACK)
        sprites.draw(screen)

        pygame.display.flip()
        clock.tick(SCREEN_FPS)


if __name__ == '__main__':
    main()
