import pygame
import snake
from Button import *

WINDOW = pygame.display.set_mode((500, 500))

b1 = Button(
    x = 100,
    y = 100,
    width = 300,
    height = 50, 
    color_rect = (88, 224, 0, 50),
    color_cursor_on_button = ()
)

while True:
    WINDOW.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    pygame.display.update()
    

# snake.Game(size_field_in_blocks = (6, 6), speed = 300).start()