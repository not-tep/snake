import pygame
import snake
import random
from InputField import *
from Button import *


WINDOW = pygame.display.set_mode((500, 300))
pygame.display.set_caption('Главное меню')

mode = 'main menu'


def set_mode_second():
    global mode
    mode = 'second menu'
    WINDOW = pygame.display.set_mode((500, 500)) 
    pygame.display.set_caption('Меню выбора режима')
def set_mode_input_size():
    global mode
    mode = 'input size'
    WINDOW = pygame.display.set_mode((500, 500)) 
    pygame.display.set_caption('Ввод меню размера поля')

def start_main_menu():
    WINDOW.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    mouse_event = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    button_play.update(mouse_event, mouse_pos)
    button_play.draw(WINDOW)

    pygame.display.flip()
def start_second_menu():
    WINDOW.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    mouse_event = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    button_play_random.update(mouse_event, mouse_pos)
    button_play_random.draw(WINDOW)
    button_input_size.update(mouse_event, mouse_pos)
    button_input_size.draw(WINDOW)

    pygame.display.flip()
def start_input_size():
    WINDOW.fill((255, 255, 255))

    mouse_event = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    input_field_width.check_mouse(mouse_event, mouse_pos)
    input_field_height.check_mouse(mouse_event, mouse_pos)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            input_field_width.update(e)
            input_field_height.update(e)

    input_field_width.draw(WINDOW)
    input_field_height.draw(WINDOW)

    pygame.display.flip()
    
def play(width = None, height = None): 
    if width == None:
        width = random.randint(4, 8)
    if height == None:
        height = random.randint(4, 8)
    result = snake.Game(size_field_in_blocks = (width, height), speed = 300).start()
    if result == pygame.K_r:
        play(width, height)
    elif result == pygame.K_m:
        global mode
        WINDOW = pygame.display.set_mode((500, 300)) 
        pygame.display.set_caption('Главное меню')
        mode = 'main menu'


button_play = Button(
    x = 100, 
    y = 100,
    width = 300,
    height = 100,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Играть',
    text_pressed = 'Играть',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 50),
    command = set_mode_second
)
button_play_random = Button(
    x = 100, 
    y = 100,
    width = 300,
    height = 100,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Случайный',
    text_pressed = 'Случайный',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 50),
    command = play
)
button_input_size = Button(
    x = 100, 
    y = 300,
    width = 300,
    height = 100,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Ввести',
    text_pressed = 'Ввести',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 50),
    command = set_mode_input_size
)
input_field_width = InputField(
    x = 100,
    y = 150,
    pad_x_text = 10,
    width = 300,
    height = 75,
    color_rect = (255, 255, 255),
    width_border = 5,
    color_border = (88, 224, 0),
    max_len_text = 2,
    default_text = 'Ширана',
    color_default_text = (125, 125, 125),
    font = pygame.font.Font('black-pixel.ttf', 50),
    color_text = (0, 0, 0),
    active_buttons = '0123456789',
    react_enter = False
)
input_field_height = InputField(
    x = 100,
    y = 275,
    pad_x_text = 10,
    width = 300,
    height = 75,
    color_rect = (255, 255, 255),
    width_border = 5,
    color_border = (88, 224, 0),
    max_len_text = 2,
    default_text = 'Высота',
    color_default_text = (125, 125, 125),
    font = pygame.font.Font('black-pixel.ttf', 50),
    color_text = (0, 0, 0),
    active_buttons = '0123456789',
    react_enter = False
)

while True:
    if mode == 'main menu':
        start_main_menu()
    elif mode == 'second menu':
        start_second_menu()
    elif mode == 'input size':
        start_input_size()

