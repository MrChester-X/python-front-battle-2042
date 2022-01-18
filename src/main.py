from src.core.field import Grid
from src.units.unit_types import load_all_unit_types
from src.enemies.enemy_types import load_all_enemy_types
from src.enemies.enemy import Enemy
from src.core.shop.shop import load_shop
from src.core.globals.main_globals import HOME_DIR, enemy_types, json_maps, FPS, SCREEN_SIZE
import pygame
import sys


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True

        # ключ уровня и сложность потом будем получать из другого класса-меню

        self.lvl = 'forest'

        self.difficulty = 'easy'

        settings = json_maps.get_json()['maps']

        find = False
        for section in settings:
            if section["key"] == self.lvl:
                settings = section
                find = True
                break

        if not find:
            print(f"Карты не существует...")
            sys.exit()

        self.grid = Grid(settings)
        print(settings)

        load_all_unit_types()
        load_all_enemy_types()
        load_shop()

        zombie1 = Enemy(list(settings['difficulties']['easy']['waves'][0].keys())[0], (0, 0))

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

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    app = Main()
    app.run()
