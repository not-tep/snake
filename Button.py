import pygame


pygame.font.init()


class Button():
    def pass_():
        pass
    def __init__(
        self,

        *,
        x: int, 
        y: int, 
        width: int, 
        height: int,
        color_rect: tuple[int, int, int],
        color_cursor_on_button: tuple[int, int, int] = None,
        color_rect_pressed: tuple[int, int, int],

        text: str = '',
        text_pressed: str = '',
        font: pygame.font.Font = pygame.font.SysFont('arial', 11),
        color_text: tuple[int, int, int] = (0, 0, 0),
        color_text_pressed: tuple[int, int, int] = (0, 0, 0),

        command = pass_,
    ) -> None:
        # Rect - button
        self.rect = pygame.Rect(x, y, width, height)
        self.color_rect = color_rect
        self.color_rect_pressed = color_rect_pressed
        self.color_cursor_on_button = color_cursor_on_button
        if self.color_cursor_on_button == None:
            self.color_cursor_on_button = self.color_rect

        # Font and text
        self.str_text = text
        self.text = font.render(self.str_text, True, (color_text))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.str_text_pressed = text_pressed
        self.text_pressed = font.render(self.str_text_pressed, True, (color_text_pressed))
        self.text_rect_pressed = self.text_pressed.get_rect()
        self.text_rect_pressed.center = self.rect.center


        self.command = command
        self.mode = 'normal'

        # 'Draw' Variables
        self.now_color_rect = self.color_rect
        self.now_text = self.text
        self.now_rect_text = self.text_rect,
    def update(self, mouse_pressed: tuple, mouse_pos: tuple) -> None:
        def set_normal(self):
            self.mode = 'normal'
            self.now_color_rect = self.color_rect
            self.now_text = self.text
            self.now_rect_text = self.text_rect
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if  mouse_pressed[0]:
                if self.mode != 'pressed':
                    self.mode = 'pressed'
                    self.now_color_rect = self.color_rect_pressed
                    self.now_text = self.text_pressed
                    self.now_rect_text = self.text_rect_pressed
            else:
                set_normal(self)
                self.now_color_rect = self.color_cursor_on_button
        else:
            set_normal(self)
            if self.mode != 'normal':
                self.command()
    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, self.now_color_rect, self.rect)
        window.blit(self.now_text, self.now_rect_text)


if __name__ == '__main__':
    def hi():
        print('Привет')
    def buy():
        print('Пока')
    b = Button(
        x = 0, 
        y = 0,
        width = 200,
        height = 100,
        color_rect = (200, 200, 200),
        color_cursor_on_button = (175, 175, 175),
        color_rect_pressed = (150, 150, 150),
        text = 'Привет',
        text_pressed = 'Пока',
        color_text = (50, 50, 50),
        color_text_pressed = (255, 255, 255),
        font = pygame.font.Font('black-pixel.ttf', 30),
        command = hi
    )

    W = pygame.display.set_mode((500, 500))

    while True:
        W.fill((255, 255, 255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        
        mouse_event = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        b.update(mouse_event, mouse_pos)
        b.draw(W)

        pygame.display.flip()
