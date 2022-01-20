from src.core.field import Grid
from src.units.unit_types import load_all_unit_types
from src.enemies.enemy_types import load_all_enemy_types
from src.enemies.enemy import Enemy
from src.core.shop.shop import load_shop
from src.core.globals.main_globals import json_maps, FPS, SCREEN_SIZE, screen, wave, sprites_loader, \
    coins, SPAWNRATE
from src.core.UI.ui_elements import Button, Text
import pygame
import sys


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FrontBattle2042")

        self.clock = pygame.time.Clock()
        self.running = False
        self.pause = False

        global wave, coins

        self.maps = json_maps.get_json()['maps']
        self.lvl_key = None
        self.difficulty = None

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.SPAWN = pygame.USEREVENT + 2

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
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 10)
        btns_y = (SCREEN_SIZE[1] // 2) - 100 // 2
        start_btn = Button(screen, (350, 100), 'Начать игру')
        exit_btn = Button(screen, (350, 100), 'Выйти')

        while menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            close_self = start_btn.draw(btns_x, btns_y - 50, events=events)
            exit_btn.draw(btns_x, btns_y + 50, sys.exit, events=events)

            if close_self:
                self.select_level()
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def select_level(self):
        menu = True
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 2) - 800 // 2
        btns_y = (SCREEN_SIZE[1] // 6)

        lvl1 = Button(screen, (800, 200),
                      f"{self.maps[0]['name']} - {self.maps[0]['description']}", 35)
        # lvl1_image = sprites_loader.load_image()

        while menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            btn0 = lvl1.draw(btns_x, btns_y, events=events)

            if btn0:
                self.lvl_key = 0
                self.select_difficulty()
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def win_screen(self):
        menu = True
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        btns_x = (SCREEN_SIZE[0] // 2) - 400 // 2
        btns_y = (SCREEN_SIZE[1] // 3) # - 100 // 2
        heading_txt = Text(screen, (255, 255, 255))
        exit_btn = Button(screen, (400, 100), 'Выйти в меню')

        while menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            heading_txt.draw('Победа!', (btns_x + 400 // 5, btns_y))
            close_self = exit_btn.draw(btns_x, btns_y + 150, events=events)

            if close_self:
                self.main_menu()
                menu = False

            pygame.display.flip()

            self.clock.tick(FPS)

    def select_difficulty(self):
        menu = True
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         ((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])))

        easy_btn = Button(screen, (200, 100), 'Easy')
        normal_btn = Button(screen, (200, 100), 'Normal')
        hard_btn = Button(screen, (200, 100), 'Hard')

        btns_x = (SCREEN_SIZE[0] // 2) - 800 // 2
        btns_y = (SCREEN_SIZE[1] // 2) - 100 // 2

        while menu:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            easy = easy_btn.draw(btns_x, btns_y - 100, events=events)
            normal = normal_btn.draw(btns_x, btns_y, events=events)
            hard = hard_btn.draw(btns_x, btns_y + 100, events=events)

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

        pygame.time.set_timer(self.SPAWN, 10)

    def add_wave(self):
        pygame.time.set_timer(self.SPAWN, SPAWNRATE)
        pygame.time.set_timer(self.COUNTDOWN, 0)
        if self.waves:
            if len(self.waves[0]) > 0:
                self.grid.add_enemy(self.waves[0].pop(0))
                print('спавн')
            else:
                print('отсчет')
                pygame.time.set_timer(self.SPAWN, 0)
                pygame.time.set_timer(self.COUNTDOWN, 1000)
                del self.waves[0]
                coins += self.wave_reward
        else:
            self.win_screen()
            print('ded')

        return 10

    def run_level(self, difficulty):
        screen.fill((0, 0, 0))
        self.generate_waves(difficulty, self.maps[self.lvl_key])

        pygame.time.set_timer(self.SPAWN, SPAWNRATE)

        wave = 1
        counter = self.add_wave()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                if event.type == self.SPAWN:
                    counter = self.add_wave()
                if event.type == self.COUNTDOWN:
                    counter -= 1
                    if counter == 0:
                        print('WAVE!')
                        counter = self.add_wave()
                        wave += 1
                    else:
                        print(counter)

            if not self.pause:
                self.grid.draw(screen)
                self.grid.update(screen)

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
