import pygame


pygame.font.init()


class Button():
    def pass_():
        pass
    def get_surf(self, color):
        surf = pygame.surface.Surface(size = (self.rect.width, self.rect.height))
        surf = self.set_alpha(surf, color)
        return surf
    def set_alpha(self, surf, color):
        try:
            surf.set_alpha(color[3])
        except IndexError:
            surf.set_alpha(255)
        return surf

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
        self.x = x
        self.y = y
        # Rect - button
        self.rect = pygame.Rect(0, 0, width, height)
        self.color_rect = color_rect
        self.color_rect_pressed = color_rect_pressed
        self.color_cursor_on_button = color_cursor_on_button
        if self.color_cursor_on_button == None:
            self.color_cursor_on_button = self.color_rect

        # Font and text
        self.text = font.render(text, True, (color_text))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
        self.set_alpha(self.text, color_text)

        self.text_pressed = font.render(text_pressed, True, (color_text_pressed))
        self.text_rect_pressed = self.text_pressed.get_rect()
        self.text_rect_pressed.center = self.rect.center
        self.set_alpha(self.text_pressed, color_text_pressed)

        self.command = command
        self.mode = 'normal'

        # Surfaces
        self.surf_rect = self.get_surf(self.color_rect)
        self.surf_rect_pressed = self.get_surf(self.color_rect_pressed)
        self.surf_cursor_on_button = self.get_surf(self.color_cursor_on_button)
        self.surf_text = self.get_surf(color_text)
        self.surf_text_pressed = self.get_surf(color_text_pressed)

        # 'Draw' Variables
        self.now_color_rect = self.color_rect
        self.now_text = self.text
        self.now_rect_text = self.text_rect
        self.now_surf_rect = self.surf_rect
        self.now_surf_text = self.surf_text

    def update(self, mouse_pressed: tuple, mouse_pos: tuple) -> None:
        def set_normal(self):
            self.mode = 'normal'
            self.now_color_rect = self.color_rect
            self.now_text = self.text
            self.now_rect_text = self.text_rect
            self.now_surf_rect = self.surf_rect
            self.now_surf_text = self.surf_text
        if pygame.Rect(self.x, self.y, self.rect.width, self.rect.height).collidepoint(mouse_pos[0], mouse_pos[1]):
            if  mouse_pressed[0]:
                self.mode = 'pressed'
                self.now_color_rect = self.color_rect_pressed
                self.now_text = self.text_pressed
                self.now_rect_text = self.text_rect_pressed
                self.now_surf_rect = self.surf_rect_pressed
                self.now_surf_text = self.surf_text_pressed
            else:
                if self.mode != 'normal':
                    self.command()
                set_normal(self)
                self.now_color_rect = self.color_cursor_on_button
                self.now_surf_rect = self.surf_cursor_on_button
        else:
            set_normal(self)
    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.rect(self.now_surf_rect, self.now_color_rect, self.rect)
        window.blit(self.now_surf_rect, (self.x, self.y))
        window.blit(self.now_text, (self.x + self.now_rect_text.x, self.y + self.now_rect_text.y))


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
        color_rect = (0, 0, 0, 200),
        color_cursor_on_button = (0, 0, 0, 215),
        color_rect_pressed = (0, 0, 0, 255),
        text = 'Привет',
        text_pressed = 'Пока',
        color_text = (50, 50, 50),
        color_text_pressed = (0, 0, 0),
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
