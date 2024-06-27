import pygame
import snake
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
def hi(): print('hi')
b = Button(
    x = 100, 
    y = 100,
    width = 300,
    height = 100,
    color_rect = (88, 224, 0, 150),
    color_cursor_on_button = (88, 224, 0, 200),
    color_rect_pressed = (88, 224, 0, 255),
    text = 'Привет',
    text_pressed = 'Пока',
    color_text = (50, 50, 50),
    color_text_pressed = (0, 0, 0),
    font = pygame.font.Font('black-pixel.ttf', 30),
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