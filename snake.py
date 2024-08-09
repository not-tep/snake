import pygame
import random
import time

pygame.font.init()


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
            return game_over('edge')
    def check_collide(self):
        try:
            all_cells[from_pos_to_num(self.rect.x, self.rect.y)].disactivate()
        except ValueError:
            return game_over('tail')
class Snake():
    def __init__(self, *blocks) -> None:
        self.blocks = list(blocks)
    def move(self) -> None:
        all_cells[from_pos_to_num(self.blocks[-1].rect.x, self.blocks[-1].rect.y)].activate()
        for i in self.blocks: i.move()
        
        x = self.blocks[0].check_out()
        if x != None: return x
        x = self.blocks[0].check_collide()
        if x != None: return x
        
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
                return win()
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


class Game():
    def __init__(self, size_field_in_blocks: tuple = (4, 4), speed: int = 300) -> None:
        create_constants(size_field_in_blocks, speed)

        global t, snake_vector, temporary_vector, all_cells, null_cells, snake, apple, all_symbols, font_ratio

        for i in range(SIZE_FIELD_IN_BLOCKS[0] * SIZE_FIELD_IN_BLOCKS[1]):
            all_cells.append(Null_cell(i % SIZE_FIELD_IN_BLOCKS[0], i // SIZE_FIELD_IN_BLOCKS[0]))

        snake = Snake(Head(SIZE_SPACE, SIZE_SPACE))
        apple = Apple()
        for i in range(3):
            draw_pause(str(3 - i), FONT_PAUSE_NUMBER, COLOR_PAUSE_TEXT)
            time.sleep(1)

    def start(self):
        return Game.run()
    def run():
        while True:
            global last_coordinate, snake_vector, t
            events()

            if t + TIME_DELAY_MOVE <= pygame.time.get_ticks():
                snake_vector = temporary_vector
                W.fill(COLOR_BACKGROUND)
                last_coordinate = (snake.blocks[-1].rect.x, snake.blocks[-1].rect.y)
                snake.replace_vector()
                x = snake.move()
                if x != None: return x
                x = apple.check_collide()
                if x != None: return x
                snake.draw()
                apple.draw()
                t = pygame.time.get_ticks()
                pygame.display.flip()

            C.tick(FPS)


# Functions

def create_constants(size_field_in_blocks, speed):
    global SIZE_BLOCK, SIZE_FIELD_IN_BLOCKS, SIZE_SPACE, SIZE_WINDOW, COLOR_BACKGROUND, COLOR_BLOCK, COLOR_APPLE, COLOR_FONT, COLOR_WIN_TEXT, COLOR_OVER_TEXT, W, C, WIN_TEXT, OVER_TEXT, FPS, TIME_DELAY_MOVE, FONT_FILE, FONT_PAUSE_NUMBER, FONT_PAUSE_TEXT, COLOR_PAUSE_TEXT, t, temporary_vector, font_ratio, all_cells, null_cells, snake_vector
    # Constants
    # Sizes
    SIZE_BLOCK = 50
    SIZE_FIELD_IN_BLOCKS = size_field_in_blocks
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
    COLOR_WIN_TEXT = (15, 135, 59)
    COLOR_OVER_TEXT = (255, 116, 0)

    # Other
    W = pygame.display.set_mode((SIZE_WINDOW[0], SIZE_WINDOW[1]))
    pygame.display.set_caption('Змейка')
    C = pygame.time.Clock()
    WIN_TEXT = ('ПОБЕДА!!!', 'УРА!!!')
    OVER_TEXT = {'edge': ('ПОКА :(', 'ТЫДЫЩ!!!'), 'tail': ('АЙ! НЕВКУСНО!', 'АЙ! БОЛЬНО В НОГЕ!')}
    FPS = 60
    TIME_DELAY_MOVE = speed

    FONT_FILE = 'black-pixel.ttf'

    # Variables
    t = pygame.time.get_ticks()
    snake_vector = (1, 0)
    temporary_vector = snake_vector

    all_symbols = '.1234567890!?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮйцукенгшщзхъфывапролджэёячсмитьбю'
    f = pygame.font.Font(FONT_FILE, 20)
    test_text = f.render(all_symbols, True, (0, 0, 0))
    font_ratio = test_text.get_width() / test_text.get_height() / len(all_symbols)
    del f, test_text
    
    FONT_PAUSE_TEXT = pygame.font.Font(FONT_FILE, int(min(SIZE_WINDOW[0] / font_ratio / len('ПАУЗА') * 0.8, SIZE_WINDOW[1] * 0.5)))
    FONT_PAUSE_NUMBER = pygame.font.Font(FONT_FILE, int(min(SIZE_WINDOW[0] * 0.5, SIZE_WINDOW[1] * 0.5)))
    COLOR_PAUSE_TEXT = (127, 127, 127)

    all_cells = []
    null_cells = []

def events() -> None:
    global temporary_vector
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                pause()
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

def draw_pause(text, font, color):
    W.fill(COLOR_BACKGROUND)
    
    text: pygame.Surface = font.render(text, True, color)
    rect_text = text.get_rect()
    rect_text.center = (SIZE_WINDOW[0] / 2, SIZE_WINDOW[1] / 2)
    snake.draw()
    apple.draw()
    
    W.blit(text, rect_text)
    pygame.display.flip()
def pause():
    global t

    draw_pause('Пауза', FONT_PAUSE_TEXT, COLOR_PAUSE_TEXT)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                for i in range(3):
                    draw_pause(str(3 - i), FONT_PAUSE_NUMBER, COLOR_PAUSE_TEXT)
                    time.sleep(1)
                t = pygame.time.get_ticks()
                return

def from_pos_to_num(x, y) -> int:
    x -= SIZE_SPACE
    y -= SIZE_SPACE
    x /= SIZE_BLOCK + SIZE_SPACE
    y /= SIZE_BLOCK + SIZE_SPACE
    return int(y * SIZE_FIELD_IN_BLOCKS[0] + x)

def win() -> None:
    snake.draw()

    text_win = random.choice(WIN_TEXT)
    create_main_text(text_win, COLOR_WIN_TEXT, W)

    size = get_size_not_main_text(2, 'r - перезапустить уровень', 'm - вернуться в меню')
    create_not_main_text('r - перезапустить уровень', size, COLOR_WIN_TEXT, 0, W)
    create_not_main_text('m - вернуться в меню', size, COLOR_WIN_TEXT, 1, W)

    pygame.display.flip()
    
    return delay_exit((pygame.K_r, pygame.K_m))
def game_over(type_over) -> None:
    snake.draw()
    apple.draw()

    text_over = random.choice(OVER_TEXT[type_over])
    create_main_text(text_over, COLOR_OVER_TEXT, W)

    size = get_size_not_main_text(2, 'r - перезапустить уровень', 'm - вернуться в меню')
    create_not_main_text('r - перезапустить уровень', size, COLOR_OVER_TEXT, 0, W)
    create_not_main_text('m - вернуться в меню', size, COLOR_OVER_TEXT, 1, W)

    W.blit(text, rect_text)
    pygame.display.flip()

    return delay_exit((pygame.K_r, pygame.K_m))

def delay_exit(codes):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key in codes:
                    return e.key
def create_main_text(text_, color, window):
    global text, rect_text
    text_str = text_
    size_text = int(min(SIZE_WINDOW[0] / font_ratio / len(text_str) * 0.8, SIZE_WINDOW[1] / 2))
    F = pygame.font.Font(FONT_FILE, size_text)
    text = F.render(text_, True, color)
    rect_text = text.get_rect()
    rect_text.center = (SIZE_WINDOW[0] // 2, (SIZE_WINDOW[1] - text.get_height()) // 2)
    window.blit(text, rect_text)
def create_not_main_text(text_, size, color, number, window):
    global text, rect_text
    F = pygame.font.Font(FONT_FILE, int(size))
    text = F.render(text_, True, color)
    rect_text = text.get_rect()
    rect_text.top = SIZE_WINDOW[1] * 0.5 + size + size * number
    rect_text.centerx = SIZE_WINDOW[0] / 2
    window.blit(text, rect_text)
def get_size_not_main_text(total_texts, *texts):
    longest = max(*texts, key = len)
    return int(min(SIZE_WINDOW[0] / font_ratio / len(longest) * 0.8, SIZE_WINDOW[1] * 0.5 / (total_texts * 2 - 1)))


if __name__ == '__main__':
    def start():
        return Game(size_field_in_blocks = (4, 2)).start()
    result = start()
    while True:
        if result == pygame.K_r:
            start()
        
