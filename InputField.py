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

        default_text: str = '',
        color_default_text: tuple[int, int, int],
        font: pygame.font.Font = pygame.font.SysFont('arial', 11),
        color_text: tuple[int, int, int] = (0, 0, 0),
        active_buttons: tuple | str = None,

        command_enter = pass_,

    ) -> None:
        self.x = x
        self.y = y
        self.pad_x_text = pad_x_text

        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.color_rect = color_rect

        self.font = font
        self.color_text = color_text
        self.text_str = ''
        self.text = self.font.render(self.text_str, True, self.color_text)
        self.active_buttons = active_buttons
        
        self.default_text = self.font.render(default_text, True, color_default_text)

        self.command_enter = command_enter
        self.mode = 'normal'
        self.timer = 0
        self.cursor = self.font.render('|', True, (127, 127, 127))
        self.cursor_index = 0

        self.x_text = self.x + self.pad_x_text
        self.y_text = self.y + (self.rect.height - self.text.get_height()) / 2
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
                self.text_str = ''
                self.text = self.font.render(self.text_str, True, self.color_text)
                self.command_enter()
                self.cursor_index = 0
                self.len_text = [0]
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
            
            try:
                if chr(event.key) in self.active_buttons:
                    pressed_symdol = chr(event.key)
                    if e.unicode == pressed_symdol.upper():
                        pressed_symdol = e.unicode
                    self.text_str = self.text_str[:self.cursor_index] + pressed_symdol + self.text_str[self.cursor_index:len(self.text_str)]
                    self.cursor_index += 1
                    self.text = self.font.render(self.text_str, True, self.color_text)
                    now_symbol = self.font.render(pressed_symdol, True, (0, 0, 0))
                    self.len_text.insert(self.cursor_index, self.len_text[self.cursor_index - 1] + now_symbol.get_width())
                    for i in range(self.cursor_index + 1, len(self.text_str) + 1):
                        self.len_text[i] += now_symbol.get_width()
                    print(self.len_text)
            except ValueError:
                pass

    def draw(self, window):
        pygame.draw.rect(window, self.color_rect, self.rect)
        if self.text_str != '':
            window.blit(self.text, (self.x_text, self.y_text))
        else:
            window.blit(self.default_text, (self.x_text, self.y_text))
        if self.mode == 'active':
            window.blit(self.cursor, (self.x_text + self.len_text[self.cursor_index] - self.cursor.get_width() / 2, self.y_text))


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
        default_text = 'Введи что-нибудь',
        color_default_text = (127, 127, 127),
        font = font,
        color_text = (0, 0, 0),
        active_buttons = '1234567890qwerty',
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