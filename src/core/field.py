import pygame
import sys


class Grid(pygame.sprite.Group):
    def __init__(self, screen_size, directories, lvl_settings=None, *sprites):
        super().__init__(*sprites)

        self.HOME_DIR = directories[0]
        self.CONFIG_DIR = directories[1]
        self.width = screen_size[0]
        self.height = screen_size[1]

        # тут надо будет либо в конфиг добавить, либо какой-то единый стандарт сделать, еще думаю
        self.TILE_SIZE = 100

        # а что с размерами сетки для тайлов делаем? пока я сколько влезет ставлю, надо подумать

        self.grid = [[0] * (self.width // self.TILE_SIZE) for _ in
                     range(self.height // self.TILE_SIZE)]

        self.description = lvl_settings['description']
        self.title = lvl_settings['name']

        self.finish = lvl_settings['enemy_line']['line_points'][-1]

        self.path_generator(lvl_settings['enemy_line']['line_points'])

    def path_generator(self, path_points):
        path_points = [[int(i[0]), int(i[1])] for i in path_points]
        # проходимся сначала по x точки, пока значение не равно x следующей точки,
        # расставляя тайлы дороги по пути, потом также с y точки
        for point in range(len(path_points) - 1):
            while path_points[point][0] < path_points[point + 1][0]:
                self.add_tile(1, (path_points[point][0], path_points[point][1]))
                path_points[point][0] += 1
            while path_points[point][1] < path_points[point + 1][1]:
                self.add_tile(1, (path_points[point][0], path_points[point][1]))
                path_points[point][1] += 1

    def update(self):
        for enemy in self.sprites():
            grid_pos = (enemy.rect.x // self.TILE_SIZE, enemy.rect.y // self.TILE_SIZE)
            if grid_pos != (int(self.finish[1]) - 1, int(self.finish[0])):
                if self.grid[grid_pos[0] + 1] and self.grid[grid_pos[1] + 1]:
                    if self.grid[grid_pos[1]][grid_pos[0] + 1] == 1:
                        enemy.move_right()
                        # print('right')
                    elif self.grid[grid_pos[1] + 1][grid_pos[0]] == 1:
                        enemy.move_down()
                        # print('down')
                    elif self.grid[grid_pos[1]][grid_pos[0] - 1] == 1:
                        enemy.move_left()
                        # print('left')
                    elif self.grid[grid_pos[1] - 1][grid_pos[0]] == 1:
                        enemy.move_up()
                        # print('up')

    def render(self, screen):
        screen.fill((0, 0, 0))
        for col in range(self.width // self.TILE_SIZE):
            for row in range(self.height // self.TILE_SIZE):
                value = self.grid[row][col]
                pygame.draw.rect(screen, pygame.Color('white'),
                                 ((col * self.TILE_SIZE, row * self.TILE_SIZE),
                                  (self.TILE_SIZE, self.TILE_SIZE)), 1)
                if value == 1:
                    pygame.draw.rect(screen, pygame.Color('cyan'),
                                     ((col * self.TILE_SIZE + 1, row * self.TILE_SIZE + 1),
                                      (self.TILE_SIZE - 2, self.TILE_SIZE - 2)))

    def add_enemy(self, *enemy):
        self.add(*enemy)

    def add_tile(self, tile, pos):
        self.grid[pos[0]][pos[1]] = tile

    def add_unit(self, unit, pos):
        pass
