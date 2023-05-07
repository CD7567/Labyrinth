import pygame
from src.core.entities import Coords


class View:
    def __init__(self, coords: Coords):
        self.x_pos, self.y_pos = coords

    def update(self, mouse_pos: Coords):
        pass


class TextView(View):
    def __init__(self, coords: Coords,
                 text: str, font: pygame.font.Font,
                 color: str,
                 window: pygame.Surface):
        super().__init__(coords)
        self.font = font
        self.color = color
        self.screen = window
        self.text = text
        self.text_render = self.font.render(self.text, True, self.color)
        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, mouse_pos: Coords):
        self.text_render = self.font.render(self.text, True, self.color)
        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))
        self.screen.blit(self.text_render, self.rect)


class Button(View):
    def __init__(self, coords: Coords,
                 text: str, font: pygame.font.Font,
                 base_color: str, hovering_color: str,
                 window: pygame.Surface):
        super().__init__(coords)
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.screen = window
        self.text = text
        self.text_render = self.font.render(self.text, True, self.base_color)
        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))

    def check_hit(self, position: Coords):
        return position[0] in range(self.rect.left, self.rect.right) \
            and position[1] in range(self.rect.top, self.rect.bottom)

    def update(self, mouse_pos: Coords):
        if self.check_hit(mouse_pos):
            self.text_render = self.font.render(self.text, True, self.hovering_color)
        else:
            self.text_render = self.font.render(self.text, True, self.base_color)
        self.screen.blit(self.text_render, self.rect)


class TextSwiper(View):
    def __init__(self, coords: Coords,
                 options: list[str], font: pygame.font.Font,
                 base_color: str, hovering_color: str,
                 window: pygame.Surface):
        super().__init__(coords)
        self.options = options
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.screen = window
        self.counter = 0
        self.text = self.options[self.counter]
        self.text_render = self.font.render(self.text, True, self.base_color)
        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))

    def check_hit(self, position):
        return position[0] in range(self.rect.left, self.rect.right) \
            and position[1] in range(self.rect.top, self.rect.bottom)

    def update(self, mouse_pos):
        if self.check_hit(mouse_pos):
            self.text_render = self.font.render(self.text, True, self.hovering_color)
        else:
            self.text_render = self.font.render(self.text, True, self.base_color)

        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))
        self.screen.blit(self.text_render, self.rect)

    def swipe(self):
        self.counter += 1
        self.text = self.options[self.counter % len(self.options)]


class EditText(View):
    def __init__(self, coords, text, default_text, font, base_color, hovering_color, window):
        super().__init__(coords)
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.screen = window
        self.default_text = default_text
        self.text = text if text else default_text
        self.buffered_text = ''
        self.text_render = self.font.render(self.text, True, self.base_color)
        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))

        self.is_being_edited = 0

    def check_hit(self, position: Coords):
        return position[0] in range(self.rect.left, self.rect.right) \
            and position[1] in range(self.rect.top, self.rect.bottom)

    def update(self, mouse_pos):
        if self.check_hit(mouse_pos) or self.is_being_edited:
            self.text_render = self.font.render(self.text, True, self.hovering_color)
        else:
            self.text_render = self.font.render(self.text, True, self.base_color)

        self.rect = self.text_render.get_rect(center=(self.x_pos, self.y_pos))
        self.screen.blit(self.text_render, self.rect)

    def start_editing(self):
        if not self.is_being_edited:
            self.is_being_edited = True
            self.buffered_text = self.text
            self.text = ''

    def finish_editing(self):
        self.is_being_edited = False
        if not self.text:
            self.text = self.default_text

    def abort_editing(self):
        self.text = self.buffered_text

    def edit(self, key: chr):
        if ord(key) in range(48, 58):
            self.text += key
        elif ord(key) == 8:
            if self.text:
                self.text = self.text[:-1]
