from src.core.globals.main_globals import MAIN_FONT
import pygame


class Text:
    def __init__(self, screen, color, font_size, font=MAIN_FONT):
        pygame.font.init()
        self.screen = screen
        self.font = pygame.font.Font(font, font_size)
        self.color = color

    def draw(self, text, pos):
        res = self.font.render(text, False, self.color)
        self.screen.blit(res, pos)


class Button:
    def __init__(self, screen, size, text, font_size=50):
        self.screen = screen
        self.width = size[0]
        self.height = size[1]

        self.font_size = font_size

        self.text_color = pygame.Color(255, 255, 255)
        self.unvisited_color = pygame.Color(0, 0, 0)
        self.visited_color = pygame.Color(255, 255, 255)

        self.message = text

        self.text = Text(screen, self.text_color, font_size)

    def draw(self, x, y, action=None):
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if x <= mouse_pos[0] <= x + self.width and y <= mouse_pos[1] <= y + self.height:
            pygame.draw.rect(self.screen, self.visited_color, ((x, y), (self.width, self.height)), 1)
            if pressed[0]:
                if action:
                    action()
        else:
            pygame.draw.rect(self.screen, self.unvisited_color, ((x, y), (self.width, self.height)))

        self.text.draw(self.message, (x + 10, y + 10))