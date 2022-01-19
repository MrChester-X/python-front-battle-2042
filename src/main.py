from src.core.field import Grid
from src.units.unit_types import load_all_unit_types
from src.enemies.enemy_types import load_all_enemy_types
from src.enemies.enemy import Enemy
from src.core.shop.shop import load_shop
from src.core.globals.main_globals import json_maps, FPS, SCREEN_SIZE
from src.core.UI.ui_elements import Button, Text
import pygame
import sys


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False

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

        self.load()

        zombie1 = Enemy(list(settings['difficulties']['easy']['waves'][0].keys())[0], (0, 0))

        self.grid.add(zombie1)

    def load(self):
        load_all_unit_types()
        load_all_enemy_types()
        load_shop()

    def main_menu(self):
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 10)  # - 350 // 2
        btns_y = (SCREEN_SIZE[1] // 2) - 100 // 2
        start_btn = Button(self.screen, (350, 100), 'Начать игру')
        exit_btn = Button(self.screen, (350, 100), 'Выйти')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            start_btn.draw(btns_x, btns_y - 50, self.run)
            exit_btn.draw(btns_x, btns_y + 50, sys.exit)

            pygame.display.flip()

            self.clock.tick(FPS)

    def run(self):
        self.screen.fill((0, 0, 0))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause

            if not self.pause:
                self.grid.draw(self.screen)
                self.grid.update()

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    app = Main()
    app.main_menu()
