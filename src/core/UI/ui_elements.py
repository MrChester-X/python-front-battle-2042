from src.core.globals.main_globals import MAIN_FONT, screen
import pygame


class Text:
    def __init__(self, screen, color, font_size=60, font=MAIN_FONT):
        pygame.font.init()
        self.screen = screen
        self.font = pygame.font.Font(font, font_size)
        self.color = pygame.Color(color[0], color[1], color[2])

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

    def draw(self, x, y, action=None, active=True, events=[]):
        mouse_pos = pygame.mouse.get_pos()

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                break

        if active:
            if x <= mouse_pos[0] <= x + self.width and y <= mouse_pos[1] <= y + self.height:
                pygame.draw.rect(self.screen, self.visited_color,
                                 ((x, y), (self.width, self.height)), 1)
                if pressed:
                    if action:
                        action()
                    return True
            else:
                pygame.draw.rect(self.screen, self.unvisited_color,
                                 ((x, y), (self.width, self.height)))
        else:
            pygame.draw.rect(self.screen, self.unvisited_color, ((x, y), (self.width, self.height)))

        self.text.draw(self.message, (x + 10, y + 10))

    def draw_shop(self, x, y, action=None, index=0, auto=False, events=[]):
        mouse_pos = pygame.mouse.get_pos()
        mouse = x <= mouse_pos[0] <= x + self.width and y <= mouse_pos[1] <= y + self.height

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                break

        if mouse or auto:
            pygame.draw.rect(self.screen, self.visited_color,
                             ((x, y), (self.width, self.height)), 1)
            if pressed and mouse:
                if action:
                    action(index)
                return True
        else:
            pygame.draw.rect(self.screen, self.unvisited_color,
                             ((x, y), (self.width, self.height)))

        self.text.draw(self.message, (x + 10, y + 10))
