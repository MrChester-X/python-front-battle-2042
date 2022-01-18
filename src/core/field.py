from src.core.globals.main_globals import TILE_SIZE, SCREEN_SIZE, GRID_SIZE, sprites_loader
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

        self.map_sprites = lvl_settings['game_settings']['sprite']

        for row in range(GRID_SIZE[1]):
            for col in range(GRID_SIZE[0]):
                self.add_tile('terrain', (col, row))

        self.path_generator(lvl_settings['enemy_line']['line_points'])

    def path_generator(self, path_points):
        path_points = [[int(i[0]), int(i[1])] for i in path_points]
        # проходимся сначала по x точки, пока значение не равно x следующей точки,
        # расставляя тайлы дороги по пути, потом также с y точки
        for point in range(len(path_points) - 1):
            while path_points[point][0] < path_points[point + 1][0]:
                self.add_tile('road', (path_points[point][0], path_points[point][1]))
                path_points[point][0] += 1
            while path_points[point][1] < path_points[point + 1][1]:
                self.add_tile('road', (path_points[point][0], path_points[point][1]))
                path_points[point][1] += 1

    def update(self):
        for enemy in self.sprites():
            if enemy.__class__ != Tile:
                grid_pos = (enemy.rect.x // TILE_SIZE, enemy.rect.y // TILE_SIZE)
                print(grid_pos == (int(self.finish[1]), int(self.finish[0]) - 1))
                if grid_pos != (int(self.finish[1]), int(self.finish[0]) - 1):
                    if self.grid[grid_pos[0] + 1] and self.grid[grid_pos[1] + 1]:
                        if self.grid[grid_pos[1]][grid_pos[0] + 1].type == 'road':
                            enemy.move_right()
                        elif self.grid[grid_pos[1] + 1][grid_pos[0]].type == 'road':
                            enemy.move_down()
                        elif self.grid[grid_pos[1]][grid_pos[0] - 1].type == 'road':
                            enemy.move_left()
                        elif self.grid[grid_pos[1] - 1][grid_pos[0]].type == 'road':
                            enemy.move_up()

    def add_enemy(self, *enemy):
        self.add(*enemy)

    def add_tile(self, tile, pos):
        tile_sprite = self.grid[pos[1]][pos[0]] = Tile(tile, pos, self.map_sprites)
        self.add(tile_sprite)

    def add_unit(self, unit, pos):
        pass


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
