import pygame
import snake
import random
from InputField import *
from Button import *


WINDOW = pygame.display.set_mode((650, 600))
pygame.display.set_caption('Главное меню')

mode = 'main menu'
list_modes = ['main menu', 'second menu', 'input size']


def set_mode_main_menu():
    global mode
    mode = 'main menu'
    pygame.display.set_mode((650, 600))
    pygame.display.set_caption('Главное меню')
def set_mode_second():
    global mode
    mode = 'second menu'
    WINDOW = pygame.display.set_mode((650, 600)) 
    pygame.display.set_caption('Меню выбора режима')
def set_mode_input_size():
    global mode
    mode = 'input size'
    WINDOW = pygame.display.set_mode((650, 600)) 
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
    button_input_size.update(mouse_event, mouse_pos)
    exit_button.update(mouse_event, mouse_pos)
    
    button_play_random.draw(WINDOW)
    button_input_size.draw(WINDOW)
    exit_button.draw(WINDOW)

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

    enter_size_button.update(mouse_event, mouse_pos)
    exit_button.update(mouse_event, mouse_pos)

    input_field_width.draw(WINDOW)
    input_field_height.draw(WINDOW)
    enter_size_button.draw(WINDOW)
    exit_button.draw(WINDOW)

    pygame.display.flip()
def back():
    global mode
    mode = list_modes[list_modes.index(mode) - 1]

def play(width = None, height = None): 
    if width == None:
        width = random.randint(4, 10)
    if height == None:
        height = random.randint(4, 10)
    result = snake.Game(size_field_in_blocks = (width, height), speed = 300).start()
    if result == pygame.K_r:
        play(width, height)
    elif result == pygame.K_m:
        set_mode_main_menu()
def analize_input_size():
    g = 0
    def check_input_field(input_field):
        nonlocal g
        if input_field.get_input() != '' and \
           2 <= int(input_field.get_input()) <= 30:
            g += 1
        else:
            input_field.set_text('')

    check_input_field(input_field_width)
    check_input_field(input_field_height)
    if g == 2:
        play(
            int(input_field_width.get_input()),
            int(input_field_height.get_input())
        )    

button_play = Button(
    x = 100, 
    y = 200,
    width = 450,
    height = 200,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Играть',
    text_pressed = 'Играть',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 100),
    command = set_mode_second
)
button_play_random = Button(
    x = 100, 
    y = 100,
    width = 450,
    height = 150,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Случайный',
    text_pressed = 'Случайный',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 70),
    command = play
)
button_input_size = Button(
    x = 100, 
    y = 350,
    width = 450,
    height = 150,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Ввести',
    text_pressed = 'Ввести',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 70),
    command = set_mode_input_size
)
input_field_width = InputField(
    x = 100,
    y = 150,
    pad_x_text = 10,
    width = 450,
    height = 75,
    color_rect = (255, 255, 255),
    width_border = 5,
    color_border = (88, 224, 0),
    max_len_text = 2,
    default_text = 'Ширина (2 - 30)',
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
    width = 450,
    height = 75,
    color_rect = (255, 255, 255),
    width_border = 5,
    color_border = (88, 224, 0),
    max_len_text = 2,
    default_text = 'Высота (2 - 30)',
    color_default_text = (125, 125, 125),
    font = pygame.font.Font('black-pixel.ttf', 50),
    color_text = (0, 0, 0),
    active_buttons = '0123456789',
    react_enter = False
)
enter_size_button = Button(
    x = 100, 
    y = 450,
    width = 450,
    height = 100,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Играть',
    text_pressed = 'Играть',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 50),
    command = analize_input_size
)
exit_button = Button(
    x = 25, 
    y = 25,
    width = 50,
    height = 50,
    color_rect = (88, 224, 0, 200),
    color_cursor_on_button = (88, 224, 0, 225),
    color_rect_pressed = (88, 224, 0, 255),
    text = '<—',
    text_pressed = '<—',
    color_text = (125, 125, 125),
    color_text_pressed = (255, 255, 255),
    font = pygame.font.Font('black-pixel.ttf', 35),
    command = back
)
# ×

while True:
    if mode == 'main menu':
        start_main_menu()
    elif mode == 'second menu':
        start_second_menu()
    elif mode == 'input size':
        start_input_size()

