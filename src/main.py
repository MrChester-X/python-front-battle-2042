import pygame
from core.field import Grid
from pathlib import Path
from src.enemies import enemies_lib
from src.config.json_controller import FileJSON
import sys


class Main:
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = 1000, 1000
        self.screen = pygame.display.set_mode(self.size)

        self.HOME_DIR = Path(__file__).resolve().parent.parent
        self.CONFIG_DIR = Path.joinpath(self.HOME_DIR, 'configs')

        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True

        self.FPS = 60

        # ключ уровня и сложность потом будем получать из другого класса-меню

        self.lvl = 'forest'

        self.difficulty = 'easy'

        try:
            self.json_controller = FileJSON(Path.joinpath(self.CONFIG_DIR, 'maps.json'))
            self.settings = \
                list(filter(lambda x: x['key'] == self.lvl,
                            self.json_controller.get_json()['maps']))[0]
        except FileNotFoundError:
            print('Файла конфигурации не существует')
            sys.exit()

        self.grid = Grid(self.size, (self.HOME_DIR, self.CONFIG_DIR), self.settings)

        zombie1 = enemies_lib.Zombie()

        self.grid.add(zombie1)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.grid.render(self.screen)

            self.grid.draw(self.screen)
            self.grid.update()

            pygame.display.flip()

            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == '__main__':
    app = Main()
    app.run()
