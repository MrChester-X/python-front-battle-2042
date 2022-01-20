from src.core.field import Grid
from src.units.unit_types import load_all_unit_types
from src.enemies.enemy_types import load_all_enemy_types
from src.enemies.enemy import Enemy
from src.core.shop.shop import load_shop
from src.core.globals.main_globals import json_maps, FPS, SCREEN_SIZE, sprites_loader, coins
from src.core.UI.ui_elements import Button, Text
import pygame
import sys


class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        self.clock = pygame.time.Clock()
        self.running = False
        self.pause = False

        self.maps = json_maps.get_json()['maps']
        self.lvl_key = None
        self.difficulty = None

        self.settings = json_maps.get_json()['maps']

        self.waves = []

        self.load()

    @staticmethod
    def load():
        load_all_unit_types()
        load_all_enemy_types()
        load_shop()

    def main_menu(self):
        menu = True
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 10)
        btns_y = (SCREEN_SIZE[1] // 2) - 100 // 2
        start_btn = Button(self.screen, (350, 100), 'Начать игру')
        exit_btn = Button(self.screen, (350, 100), 'Выйти')

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            close_self = start_btn.draw(btns_x, btns_y - 50)
            exit_btn.draw(btns_x, btns_y + 50, sys.exit)

            if close_self:
                self.select_level()
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def select_level(self):
        menu = True
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 2) - 800 // 2
        btns_y = (SCREEN_SIZE[1] // 6)

        lvl1 = Button(self.screen, (800, 200),
                      f"{self.maps[0]['name']} - {self.maps[0]['description']}", 35)
        # lvl1_image = sprites_loader.load_image()

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            btn0 = lvl1.draw(btns_x, btns_y)

            if btn0:
                self.lvl_key = 0
                self.select_difficulty()
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def select_difficulty(self):
        menu = True
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        easy_btn = Button(self.screen, (200, 100), 'Easy')
        normal_btn = Button(self.screen, (200, 100), 'Normal')
        hard_btn = Button(self.screen, (200, 100), 'Hard')

        btns_x = (SCREEN_SIZE[0] // 2) - 800 // 2
        btns_y = (SCREEN_SIZE[1] // 2) - 100 // 2

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            easy = easy_btn.draw(btns_x, btns_y - 100)
            normal = normal_btn.draw(btns_x, btns_y)
            hard = hard_btn.draw(btns_x, btns_y + 100)

            if easy:
                res = 'easy'
            elif normal:
                res = 'normal'
            elif hard:
                res = 'hard'

            if easy or normal or hard:
                self.grid = Grid(self.maps[self.lvl_key])
                self.running = True
                self.run_level(res)
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def generate_waves(self, difficulty, lvl):
        settings = lvl['difficulties'][difficulty]
        self.wave_reward = settings['prize']
        for wave in settings['waves']:
            enemies = []
            for enemy_type in wave:
                for enemy in range(wave[enemy_type]):
                    enemies.append(Enemy(enemy_type, (0, 0)))
            self.waves.append(enemies)

        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 1000)

    def run_level(self, difficulty):
        self.screen.fill((0, 0, 0))
        self.generate_waves(difficulty, self.maps[self.lvl_key])
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                if event.type == self.ADDENEMY:
                    if len(self.waves) > 0:
                        if len(self.waves[0]) > 1:
                            self.grid.add(self.waves[0].pop(0))
                        elif len(self.waves[0]) == 1:
                            self.grid.add(self.waves[0].pop(0))
                            del self.waves[0]
                    else:
                        self.running = False

            if not self.pause:
                self.grid.draw(self.screen)
                self.grid.update()

            if self.grid.base.health <= 0:
                self.main_menu()
                self.running = False
                return

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    app = Main()
    app.main_menu()
