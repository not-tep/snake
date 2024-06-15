import pygame
import random


pygame.font.init()


# Constants
# Sizes
SIZE_BLOCK = 50
SIZE_FIELD_IN_BLOCKS = (2, 2)
SIZE_SPACE = 10
SIZE_WINDOW = (
    (SIZE_BLOCK + SIZE_SPACE) * SIZE_FIELD_IN_BLOCKS[0] + SIZE_SPACE,
    (SIZE_BLOCK + SIZE_SPACE) * SIZE_FIELD_IN_BLOCKS[1] + SIZE_SPACE
)

# Colors
COLOR_BACKGROUND = (255, 255, 255)
COLOR_BLOCK = (0, 255, 0)
COLOR_APPLE = (255, 0, 0)
COLOR_FONT = (0, 182, 63)
COLOR_WIN_TEXT = (0, 185, 69)
COLOR_OVER_TEXT = (255, 116, 0)


# Other
W = pygame.display.set_mode((SIZE_WINDOW[0], SIZE_WINDOW[1]))
C = pygame.time.Clock()
WIN_TEXT = ('ПОБЕДА!!!', 'УРА!!!')
OVER_TEXT = {'edge': ('ПОКА :(', 'ТЫДЫЩ!!!'), 'tail': ('АЙ! НЕВКУСНО!', 'АЙ! БОЛЬНО В НОГЕ!')}
FPS = 60
TIME_DELAY_MOVE = 300
FONT_FILE = 'black-pixel.ttf'


t = pygame.time.get_ticks()
snake_vector = (1, 0)
temporary_vector = snake_vector


# Classes
class Block():
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(x, y, SIZE_BLOCK, SIZE_BLOCK)
    def move(self) -> None:
        self.rect.x += (SIZE_BLOCK + SIZE_SPACE) * self.vector[0]
        self.rect.y += (SIZE_BLOCK + SIZE_SPACE) * self.vector[1]
    def draw(self) -> None:
        pygame.draw.rect(W, COLOR_BLOCK, self.rect)
        pygame.draw.rect(W, COLOR_BLOCK, (
            self.rect.x + SIZE_SPACE * self.space_vector[0],
            self.rect.y + SIZE_SPACE * self.space_vector[1],
            self.rect.width,
            self.rect.height
        ))
class Head(Block):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        global null_cells
        self.vector = snake_vector
        self.space_vector = (0, 0)
        all_cells[from_pos_to_num(self.rect.x, self.rect.y)].disactivate()
    def check_out(self):
        if self.rect.x >= SIZE_WINDOW[0] or self.rect.x < 0 or self.rect.y >= SIZE_WINDOW[1] or self.rect.y < 0:
            game_over('edge')
    def check_collide(self):
        try:
            all_cells[from_pos_to_num(self.rect.x, self.rect.y)].disactivate()
        except ValueError:
            game_over('tail')
class Snake():
    def __init__(self, *blocks) -> None:
        self.blocks = list(blocks)
    def move(self) -> None:
        all_cells[from_pos_to_num(self.blocks[-1].rect.x, self.blocks[-1].rect.y)].activate()
        for i in self.blocks:
            i.move()
        self.blocks[0].check_out()
        self.blocks[0].check_collide()
        
    def replace_vector(self) -> None:
        for i in range(len(self.blocks) - 1, 0, -1):
            self.blocks[i].vector = self.blocks[i - 1].vector
        self.blocks[0].vector = snake_vector
        for i in range(len(self.blocks) - 1, 0, -1):
            self.blocks[i].space_vector = self.blocks[i - 1].vector
    def draw(self) -> None:
        for i in self.blocks:
            i.draw()
    def add_block(self) -> None:
        self.blocks.append(Block(last_coordinate[0], last_coordinate[1]))
        self.blocks[-1].vector = self.blocks[-2].vector
        self.blocks[-1].space_vector = self.blocks[-2].vector
        all_cells[from_pos_to_num(self.blocks[-1].rect.x, self.blocks[-1].rect.y)].disactivate()
class Apple():
    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, SIZE_BLOCK, SIZE_BLOCK)
        self.replace_pos() 
    def check_collide(self):
        if self.rect.colliderect(snake.blocks[0]):
            snake.add_block()
            if len(null_cells) == 0:
                win()
            self.replace_pos()
    def replace_pos(self):
        pos = random.choice(null_cells)
        self.rect.topleft = (pos[0] * (SIZE_BLOCK + SIZE_SPACE) + SIZE_SPACE, pos[1] * (SIZE_BLOCK + SIZE_SPACE) + SIZE_SPACE)
     
    def draw(self) -> None:
        pygame.draw.rect(W, COLOR_APPLE, self.rect)
class Null_cell():
    def __init__(self, row, collumn) -> None:
        self.row = row
        self.collumn = collumn
        self.coordinates = (self.row, self.collumn)
        self.activate()
    def activate(self):
        global null_cells
        null_cells.append(self.coordinates)
    def disactivate(self):
        global null_cells
        null_cells.remove(self.coordinates)


# Functions
def events() -> None:
    global temporary_vector
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if snake_vector != (0, 1):
                    temporary_vector = (0, -1)
            if e.key == pygame.K_DOWN:
                if snake_vector != (0, -1):
                    temporary_vector = (0, 1)
            if e.key == pygame.K_RIGHT:
                if snake_vector != (-1, 0):
                    temporary_vector = (1, 0)
            if e.key == pygame.K_LEFT:
                if snake_vector != (1, 0):
                    temporary_vector = (-1, 0)
def from_pos_to_num(x, y) -> int:
    x -= SIZE_SPACE
    y -= SIZE_SPACE
    x /= SIZE_BLOCK + SIZE_SPACE
    y /= SIZE_BLOCK + SIZE_SPACE
    return int(y * SIZE_FIELD_IN_BLOCKS[0] + x)
def win():
    text_win = random.choice(WIN_TEXT)
    f = pygame.font.Font(FONT_FILE, 20)
    test_text = f.render(text_win, True, (0, 0, 0))
    F = pygame.font.Font(FONT_FILE, int(SIZE_WINDOW[0] * 0.8 / test_text.get_width() * test_text.get_height()))
    text = F.render(text_win, True, COLOR_WIN_TEXT)
    del f, test_text

    snake.draw()
    W.blit(text, ((SIZE_WINDOW[0] - text.get_width()) / 2, (SIZE_WINDOW[1] - text.get_height()) / 2))
    pygame.display.flip()
    delay_exit()
def game_over(type_over):
    text_over = random.choice(OVER_TEXT[type_over])
    f = pygame.font.Font(FONT_FILE, 20)
    test_text = f.render(text_over, True, (0, 0, 0))
    F = pygame.font.Font(FONT_FILE, int(SIZE_WINDOW[0] * 0.8 / test_text.get_width() * test_text.get_height()))
    text = F.render(text_over, True, COLOR_OVER_TEXT)
    del f, test_text

    snake.draw()
    apple.draw()
    W.blit(text, ((SIZE_WINDOW[0] - text.get_width()) / 2, (SIZE_WINDOW[1] - text.get_height()) / 2))
    pygame.display.flip()
    delay_exit()
def delay_exit():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()


all_cells = []
null_cells = []
for i in range(SIZE_FIELD_IN_BLOCKS[0] * SIZE_FIELD_IN_BLOCKS[1]):
    all_cells.append(Null_cell(i % SIZE_FIELD_IN_BLOCKS[0], i // SIZE_FIELD_IN_BLOCKS[0]))

snake = Snake(Head(SIZE_SPACE, SIZE_SPACE))
apple = Apple()

win()
# Game circle
while True:
    events()

    if t + TIME_DELAY_MOVE <= pygame.time.get_ticks():
        snake_vector = temporary_vector
        W.fill(COLOR_BACKGROUND)
        last_coordinate = (snake.blocks[-1].rect.x, snake.blocks[-1].rect.y)
        snake.replace_vector()
        snake.move()
        apple.check_collide()
        snake.draw()
        apple.draw()
        t = pygame.time.get_ticks()
        pygame.display.flip()

    C.tick(FPS)
