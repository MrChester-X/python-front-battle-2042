import sys

import pygame
from pathlib import Path


class Grid:
    def __init__(self, screen_size, directories, lvl_config=None):
        self.HOME_DIR = directories[0]
        self.CONFIG_DIR = directories[1]
        self.width = screen_size[0]
        self.height = screen_size[1]

        try:
            with open(Path.joinpath(self.CONFIG_DIR, lvl_config)) as grid_config:
                pass

        except FileNotFoundError:
            print('Файла конфигурации не существует')
            sys.exit()
