from src.core.globals.main_globals import TILE_SIZE, SCREEN_SIZE, GRID_SIZE, sprites_loader
from src.core.UI.ui_elements import Text
from src.core.globals.main_globals import coins, screen as sc, wave
import pygame


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

        self.wave_text = Text(sc, (255, 255, 255))
        self.coin_text = Text(sc, (255, 255, 255))

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

    def update(self, screen):
        for enemy in self.sprites():
            if enemy.__class__ != Tile:
                grid_pos = (enemy.rect.x // TILE_SIZE, enemy.rect.y // TILE_SIZE)
                if grid_pos != (int(self.finish[0]), int(self.finish[1])):
                    if grid_pos[1] + 1 and self.grid[grid_pos[1] + 1][grid_pos[0]].type == 'road':
                        enemy.move_down()
                    # elif grid_pos[0] - 1 and self.grid[grid_pos[1]][grid_pos[0] - 1].type == 'road':
                    #     enemy.move_left()
                    elif grid_pos[0] + 1 and self.grid[grid_pos[1]][grid_pos[0] + 1].type == 'road':
                        enemy.move_right()
                    elif grid_pos[1] - 1 and self.grid[grid_pos[1] - 1][grid_pos[0]].type == 'road':
                        enemy.move_up()
                else:
                    print("атака")
                    enemy.attack(self.base)
                    break

        self.wave_text.draw(f"Волна: {wave}", (10, 600))
        self.coin_text.draw(f"Деньги: {coins}", (10, 650))

    def add_enemy(self, *enemy):
        self.add(*enemy)

    def add_tile(self, tile, pos):
        tile_sprite = self.grid[pos[1]][pos[0]] = Tile(tile, pos, self.map_sprites)
        self.add(tile_sprite)

    def add_unit(self, unit, pos):
        pass

    # def regenerate(self):
    #     super().__init__()


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
