import pygame
from pygame.font import Font, SysFont

pygame.font.init()

class InputField():
    def pass_(cls):
        pass
    def __init__(
        self,
        *,
        x: int, 
        y: int,
        pad_x_text: int,

        width: int, 
        height: int,
        color_rect: tuple[int, int, int],
        width_border: int = 0,
        color_border: tuple[int, int, int] = (0, 0, 0),

        max_len_text: int|None = None,
        default_text: str = '',
        color_default_text: tuple[int, int, int],
        font: pygame.font.Font = pygame.font.SysFont('arial', 11),
        color_text: tuple[int, int, int] = (0, 0, 0),
        active_buttons: tuple | str | None = None, # Stay 'None' to get pressing all keys 

        react_enter: bool = True,
        command_enter = pass_,

    ) -> None:
        self.x = x
        self.y = y
        self.pad_x_text = pad_x_text

        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.draw_rect = pygame.rect.Rect(0, 0, width, height)
        self.color_rect = color_rect
        self.width_border = width_border
        self.color_border = color_border
        self.surf = pygame.Surface((width, height))

        self.max_len_text = max_len_text
        self.font = font
        self.color_text = color_text
        self.text_str = ''
        self.text = self.font.render(self.text_str, True, self.color_text)
        self.active_buttons = active_buttons
        
        self.default_text = self.font.render(default_text, True, color_default_text)

        self.react_enter = react_enter
        self.command_enter = command_enter
        self.mode = 'normal'
        self.timer = 0
        self.cursor = self.font.render('|', True, (127, 127, 127))
        self.cursor_index = 0

        self.x_text = self.pad_x_text
        self.y_text = (self.rect.height - self.text.get_height()) / 2
        self.len_text = [0]
    def check_mouse(self, mouse_click, mouse_pos):
        if mouse_click[0]:
            if self.rect.collidepoint(mouse_pos):
                self.mode = 'active'
                if self.mode != 'active':
                    self.timer = pygame.time.get_ticks()
            else:
                self.mode = 'normal'
    def update(self, event):
        if self.mode == 'active':
            if event.key == pygame.K_RETURN:
                if self.react_enter:
                    text_str = self.text_str
                    self.text_str = ''
                    self.text = self.font.render(self.text_str, True, self.color_text)
                    self.command_enter()
                    self.cursor_index = 0
                    self.len_text = [0]
                    return text_str
                return
            
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_index > 0:
                    deleting_symbol = self.font.render(str(self.text_str[self.cursor_index - 1]), True, (0, 0, 0))
                    self.text_str = self.text_str[:self.cursor_index - 1] + self.text_str[self.cursor_index:len(self.text_str)]
                    self.cursor_index -= 1
                    self.text = self.font.render(self.text_str, True, self.color_text)
                    self.len_text.pop(self.cursor_index)
                    for i in range(self.cursor_index, len(self.len_text)):
                        self.len_text[i] -= deleting_symbol.get_width()
                return
            
            if event.key == pygame.K_LEFT:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                return
            
            if event.key == pygame.K_RIGHT:
                if self.cursor_index < len(self.text_str):
                    self.cursor_index += 1
                return
            
            if event.key == pygame.K_ESCAPE:
                self.mode = 'normal'
                return
            
            try:
                chr(event.key)
                if not self.active_buttons or chr(event.key) in self.active_buttons:
                    if not self.max_len_text or len(self.text_str) < self.max_len_text:
                        pressed_symdol = event.unicode
                        self.text_str = self.text_str[:self.cursor_index] + pressed_symdol + self.text_str[self.cursor_index:len(self.text_str)]
                        self.cursor_index += 1
                        self.text = self.font.render(self.text_str, True, self.color_text)
                        now_symbol = self.font.render(pressed_symdol, True, (0, 0, 0))
                        self.len_text.insert(self.cursor_index, self.len_text[self.cursor_index - 1] + now_symbol.get_width())
                        for i in range(self.cursor_index + 1, len(self.text_str) + 1):
                            self.len_text[i] += now_symbol.get_width()
            except ValueError:
                pass
    def draw(self, window):
        pygame.draw.rect(self.surf, self.color_border, self.draw_rect, self.width_border)
        pygame.draw.rect(self.surf, self.color_rect, (
            self.width_border, 
            self.width_border, 
            self.rect.width - self.width_border * 2,
            self.rect.height - self.width_border * 2
        ))
        if self.text_str != '':
            self.surf.blit(self.text, (self.x_text, self.y_text))
        else:
            self.surf.blit(self.default_text, (self.x_text, self.y_text))
        if self.mode == 'active':
            self.surf.blit(self.cursor, (self.x_text + self.len_text[self.cursor_index] - self.cursor.get_width() / 2, self.y_text))
        window.blit(self.surf, (self.x, self.y))

    def get_input(self):
        return self.text_str
    def set_text(self, text):
        self.text_str = text
        self.text = self.font.render(self.text_str, True, self.color_text)

if __name__ == '__main__':
    window = pygame.display.set_mode((550, 80))
    font = pygame.font.Font('black-pixel.ttf', 40)
    def good(): print('good!')
    if1 = InputField(
        x = 5,
        y = 5,
        pad_x_text = 5,
        width = 500,
        height = 50,
        color_rect = (255, 255, 255),
        max_len_text = 2,
        default_text = 'Введи что-нибудь',
        color_default_text = (127, 127, 127),
        font = font,
        color_text = (0, 0, 0),
        react_enter = False,
        command_enter = good
    )
    while True:
        if1.check_mouse(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if1.update(e)

        
        window.fill((200, 255, 200))
        if1.draw(window)
        pygame.display.flip()