import pygame
import sys
import random


class Snake(object):
    def __init__(self):
        self.length = 1
        self.position = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (0, 0, 0)  # rgb
        self.score = 0

    def head_position(self):
        return self.position[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.head_position()
        x, y = self.direction
        new = (((cur[0] + (x * grid_size)) % screen_width), (cur[1] + (y * grid_size)) % screen_height)
        if len(self.position) > 2 and new in self.position[2:]:
            self.reset()
        else:
            self.position.insert(0, new)
            if len(self.position) > self.length:
                self.position.pop()

    def reset(self):
        self.length = 1
        self.position = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for p in self.position:
            r = pygame.Rect((p[0], p[1]), (grid_size, grid_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


class Food(object):
    def __init__(self):
        self.f_position = (0, 0)
        self.color = (6, 229, 229)
        self.random_position()

    def random_position(self):
        self.f_position = (
            random.randint(0, grid_width - 1) * grid_size, random.randint(0, grid_height - 1) * grid_size)

    def draw(self, surface):
        r = pygame.Rect((self.f_position[0], self.f_position[1]), (grid_size, grid_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (6, 229, 229), r, 1)


def draw_grid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
                pygame.draw.rect(surface, (91, 91, 91), r)
            else:
                rr = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
                pygame.draw.rect(surface, (140, 140, 140), rr)


# global var

screen_width = 480
screen_height = 480

grid_size = 30
grid_width = screen_height / grid_size
grid_height = screen_width / grid_size

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def main():
    pygame.init()
    pygame.display.set_caption('Simple Snake Game')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()

    font = pygame.font.SysFont("Helvetica", 25)

    while True:
        clock.tick(10)
        snake.handle_keys()
        draw_grid(surface)
        snake.move()
        if snake.head_position() == food.f_position:
            snake.length += 1
            snake.score += 1
            food.random_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = font.render("Score {0}".format(snake.score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()


main()
