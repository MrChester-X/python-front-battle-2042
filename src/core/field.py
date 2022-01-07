import pygame
import sys
from src.config.json_controller import FileJSON
from pathlib import Path


class Grid:
    def __init__(self, screen_size, directories, difficulty, lvl_key=None):
        self.HOME_DIR = directories[0]
        self.CONFIG_DIR = directories[1]
        self.width = screen_size[0]
        self.height = screen_size[1]

        # тут надо будет либо в конфиг добавить, либо какой-то единый стандарт сделать, еще думаю
        self.TILE_SIZE = 100

        # а что с размерами сетки для тайлов делаем? пока я сколько влезет ставлю, надо подумать

        self.grid = [[0] * (self.width // self.TILE_SIZE) for _ in
                     range(self.height // self.TILE_SIZE)]

        try:
            self.json_controller = FileJSON(Path.joinpath(self.CONFIG_DIR, 'maps.json'))
            settings = \
                list(filter(lambda x: x['key'] == lvl_key,
                            self.json_controller.get_json()['maps']))[0]

            self.path_generator(settings['enemy_line']['line_points'])

            self.description = settings['description']
            self.title = settings['name']

            self.enemies = []

        except FileNotFoundError:
            print('Файла конфигурации не существует')
            sys.exit()

    def path_generator(self, path_points):
        path_points = [[int(i[0]), int(i[1])] for i in path_points]
        # проходимся сначала по x точки, пока значение не равно x следующей точки,
        # расставляя тайлы дороги по пути, потом также с y точки
        for point in range(len(path_points) - 1):
            while path_points[point][0] < path_points[point + 1][0]:
                self.set_tile(1, (path_points[point][0], path_points[point][1]))
                path_points[point][0] += 1
            while path_points[point][1] < path_points[point + 1][1]:
                self.set_tile(1, (path_points[point][0], path_points[point][1]))
                path_points[point][1] += 1

    def set_tile(self, tile, coords):
        self.grid[coords[0]][coords[1]] = tile

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        for col in range(self.width // self.TILE_SIZE):
            for row in range(self.height // self.TILE_SIZE):
                value = self.grid[row][col]
                print(value)
                pygame.draw.rect(screen, pygame.Color('white'),
                                 ((col * self.TILE_SIZE, row * self.TILE_SIZE),
                                  (self.TILE_SIZE, self.TILE_SIZE)), 1)
                if value == 1:
                    pygame.draw.rect(screen, pygame.Color('cyan'),
                                     ((col * self.TILE_SIZE + 1, row * self.TILE_SIZE + 1),
                                      (self.TILE_SIZE - 2, self.TILE_SIZE - 2)))
