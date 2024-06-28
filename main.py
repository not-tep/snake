import pygame
import snake
import random
from Button import *

WINDOW = pygame.display.set_mode((500, 500))

# b1 = Button(
#     x = 0,
#     y = 0,
#     width = 300,
#     height = 50, 
#     color_rect = (88, 224, 0, 50),
#     color_cursor_on_button = (),
#     color_rect_pressed = (88, 224, 0, 50),
# )
def hi(width = None, height = None): 
    if width == None:
        width = random.randint(5, 5)
    if height == None:
        height = random.randint(5, 5)
    result = snake.Game(size_field_in_blocks = (width, height), speed = 300).start()
    if result == pygame.K_r:
        hi(width, height)
    elif result == pygame.K_m:
        WINDOW = pygame.display.set_mode((500, 500))


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
    color_text_pressed = (25, 25, 25),
    font = pygame.font.Font('black-pixel.ttf', 50),
    command = hi
)

while True:
    WINDOW.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    mouse_event = pygame.mouse.get_pressed()
    # print(mouse_event)
    mouse_pos = pygame.mouse.get_pos()
    # print(mouse_pos)
    b.update(mouse_event, mouse_pos)
    b.draw(WINDOW)

    pygame.display.flip()
    

# snake.Game(size_field_in_blocks = (6, 6), speed = 300).start()