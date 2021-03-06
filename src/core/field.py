from math import sqrt

from src.core.globals.main_globals import TILE_SIZE, SCREEN_SIZE, GRID_SIZE, sprites_loader
from src.core.UI.ui_elements import Text, Button
from src.core.globals.main_globals import wave, coins, screen as sc, unit_types
from src.enemies.enemy import Enemy
import pygame

from src.units.unit import Unit


class Grid(pygame.sprite.Group):
    def __init__(self, lvl_settings=None, *sprites):
        super().__init__(*sprites)

        self.width = SCREEN_SIZE[0]
        self.height = SCREEN_SIZE[1]

        self.grid = [[0] * GRID_SIZE[0] for _ in range(GRID_SIZE[1])]

        self.description = lvl_settings['description']
        self.title = lvl_settings['name']

        self.finish = lvl_settings['enemy_line']['line_points'][-1]

        base = (int(lvl_settings['enemy_line']['line_points'][-1][0]),
                int(lvl_settings['enemy_line']['line_points'][-1][1]))

        self.base = self.grid[base[1]][base[0]] = Base()

        self.map_sprites = lvl_settings['game_settings']['sprite']

        for row in range(GRID_SIZE[1]):
            for col in range(GRID_SIZE[0]):
                self.add_tile('terrain', (col, row))

        self.path_generator(lvl_settings['enemy_line']['line_points'])

        self.wave_text = Text(sc, (255, 255, 255), font_size=30)
        self.coin_text = Text(sc, (255, 255, 255), font_size=30)
        self.enemy_text = Text(sc, (255, 255, 255), font_size=30)

        self.units_buy = []
        self.unit_choosen = 1
        for key, value in unit_types.items():
            self.units_buy.append([key, Button(sc, (350, 70), f"{value.name} ({value.cost}$)", font_size=40)])

    def path_generator(self, path_points):
        path_points = [[int(i[0]), int(i[1])] for i in path_points]

        for point in path_points:
            self.add_tile('road', (point[0], point[1]))

        # for point in range(len(path_points) - 1):
        #     while path_points[point][0] < path_points[point + 1][0]:
        #         self.add_tile('road', (path_points[point][0], path_points[point][1]))
        #         path_points[point][0] += 1
        #     while path_points[point][1] < path_points[point + 1][1]:
        #         self.add_tile('road', (path_points[point][0], path_points[point][1]))
        #         path_points[point][1] += 1

    def update(self, screen, events):
        global coins
        global wave

        flag = False
        for model in self.sprites():
            grid_pos = (model.rect.x // TILE_SIZE, model.rect.y // TILE_SIZE)
            if model.__class__ == Enemy:
                mouse_pos = pygame.mouse.get_pos()
                enemy_pos = (model.rect.x + TILE_SIZE // 2, model.rect.y + TILE_SIZE // 2)
                distance = sqrt((mouse_pos[0] - enemy_pos[0]) ** 2 + (mouse_pos[1] - enemy_pos[1]) ** 2)
                if distance <= TILE_SIZE and not flag:
                    self.enemy_text.draw(f"{round(model.health, 1)}/{round(model.max_health, 1)}", (950, 750))
                    flag = True

                if grid_pos != (int(self.finish[0]), int(self.finish[1])):
                    if grid_pos[1] + 1 and self.grid[grid_pos[1] + 1][grid_pos[0]].type == 'road':
                        model.move_down()
                    # elif grid_pos[0] - 1 and self.grid[grid_pos[1]][grid_pos[0] - 1].type == 'road':
                    #     enemy.move_left()
                    elif grid_pos[0] + 1 and self.grid[grid_pos[1]][grid_pos[0] + 1].type == 'road':
                        model.move_right()
                    elif grid_pos[1] - 1 and self.grid[grid_pos[1] - 1][grid_pos[0]].type == 'road':
                        model.move_up()
                else:
                    print("??????????")
                    model.attack(self.base)
                    break
            elif model.__class__ == Unit:
                unit_pos = (model.pos[0] + TILE_SIZE // 2, model.pos[1] + TILE_SIZE // 2)
                radius = unit_types[model.type].radius * TILE_SIZE
                pygame.draw.circle(screen, (0, 0, 0), unit_pos, radius, 2)
                for enemy in self.sprites():
                    if enemy.__class__ != Enemy:
                        continue

                    enemy_pos = (enemy.rect.x + TILE_SIZE // 2, enemy.rect.y + TILE_SIZE // 2)
                    distance = sqrt((unit_pos[0] - enemy_pos[0]) ** 2 + (unit_pos[1] - enemy_pos[1]) ** 2)
                    if distance > radius:
                        continue

                    enemy.health -= unit_types[model.type].damage
                    if int(enemy.health + unit_types[model.type].damage) > int(enemy.health):
                        coins += 1
                    if enemy.health < 0:
                        enemy.remove(self)
                    break

        self.wave_text.draw(f"??????????: {wave}", (10, 600))
        self.coin_text.draw(f"????????????: {coins}", (10, 640))

        x, y, c = 300, 600, 0
        for i, unit in enumerate(self.units_buy):
            unit[1].draw_shop(x, y, events=events, auto=(self.unit_choosen == i), index=i, action=self.choose_unit)

            c += 1
            if c <= 1:
                y += 70
            else:
                y -= 70
                x += 350

        self.check_buy(events)

    def choose_unit(self, index):
        if self.unit_choosen == index:
            self.unit_choosen = -1
        else:
            self.unit_choosen = index

    def check_buy(self, events):
        global coins

        if self.unit_choosen == -1:
            return

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                break

        if not pressed:
            return

        mouse_pos = pygame.mouse.get_pos()
        grid_pos = (mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE)
        if grid_pos[0] >= GRID_SIZE[0] or grid_pos[1] >= GRID_SIZE[1]:
            return

        print(self.grid[grid_pos[1]][grid_pos[0]].type)

        if self.grid[grid_pos[1]][grid_pos[0]].type != "terrain":
            return

        unit = unit_types[self.units_buy[self.unit_choosen][0]]
        if coins < unit.cost:
            return

        # ?????? ?????????????? ????????????

        not_good_code = self.sprites()
        for good_code in not_good_code:
            if good_code.__class__ == Unit:
                if good_code.rect.x // TILE_SIZE == grid_pos[0]:
                    if good_code.rect.y // TILE_SIZE == grid_pos[1]:
                        if True:
                            if not False:
                                good_code.remove(self)

        self.add_unit(unit, grid_pos)

    def add_enemy(self, *enemy):
        self.add(*enemy)

    def add_tile(self, tile, pos):
        tile_sprite = self.grid[pos[1]][pos[0]] = Tile(tile, pos, self.map_sprites)
        self.add(tile_sprite)

    def add_unit(self, unit, pos):
        global coins
        self.add(Unit(unit.key, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)))
        coins -= unit.cost


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos, sprites):
        super().__init__()

        self.type = type
        self.pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

        self.load_sprite(sprites)

    def load_sprite(self, sprites):
        self.image = sprites_loader.load_image(sprites[self.type])
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Base:
    def __init__(self):
        self.health = 1


def set_wave(count):
    global wave
    wave = count


def get_wave():
    return wave


def set_coins(count):
    global coins
    coins = count
