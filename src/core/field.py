from src.core.globals.main_globals import HOME_DIR, TILE_SIZE, SCREEN_SIZE, GRID_SIZE
import pygame


class Grid(pygame.sprite.Group):
    def __init__(self, lvl_settings=None, *sprites):
        super().__init__(*sprites)

        self.width = SCREEN_SIZE[0]
        self.height = SCREEN_SIZE[1]

        # тут надо будет либо в конфиг добавить, либо какой-то единый стандарт сделать, еще думаю

        # а что с размерами сетки для тайлов делаем? пока я сколько влезет ставлю, надо подумать

        self.grid = [[0] * GRID_SIZE[0] for _ in range(GRID_SIZE[1])]

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
            grid_pos = (enemy.rect.x // TILE_SIZE, enemy.rect.y // TILE_SIZE)
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
        for col in range(GRID_SIZE[0]):
            for row in range(GRID_SIZE[1]):
                value = self.grid[row][col]
                pygame.draw.rect(screen, pygame.Color('white'),
                                 ((col * TILE_SIZE, row * TILE_SIZE),
                                  (TILE_SIZE, TILE_SIZE)), 1)
                if value == 1:
                    pygame.draw.rect(screen, pygame.Color('cyan'),
                                     ((col * TILE_SIZE + 1, row * TILE_SIZE + 1),
                                      (TILE_SIZE - 2, TILE_SIZE - 2)))

    def add_enemy(self, *enemy):
        self.add(*enemy)

    def add_tile(self, tile, pos):
        self.grid[pos[0]][pos[1]] = tile

    def add_unit(self, unit, pos):
        pass
