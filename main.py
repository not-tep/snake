import pygame
import snake
import random
from Button import *

WINDOW = pygame.display.set_mode((500, 300))
pygame.display.set_caption('Главное меню')

def play(width = None, height = None): 
    if width == None:
        width = random.randint(4, 8)
    if height == None:
        height = random.randint(4, 8)
    result = snake.Game(size_field_in_blocks = (width, height), speed = 300).start()
    if result == pygame.K_r:
        play(width, height)
    elif result == pygame.K_m:
        WINDOW = pygame.display.set_mode((500, 300)) 


b = Button(
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
    command = play
)

while True:
    WINDOW.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    mouse_event = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    b.update(mouse_event, mouse_pos)
    b.draw(WINDOW)

    pygame.display.flip()
    
