import pygame

from src.config.json_controller import FileJSON
from src.config.image_controller import ImageLoader
from pathlib import Path

SCREEN_SIZE = width, height = 1200, 800
GRID_SIZE = (12, 6)
FPS = 60
TILE_SIZE = 100
HOME_DIR = Path(__file__).resolve().parent.parent.parent.parent
MAIN_FONT = Path().joinpath(HOME_DIR, 'src', 'core', 'UI', 'fonts', 'JETBRAINS.ttf')

json_units = FileJSON(Path.joinpath(HOME_DIR, "configs/units.json"))
json_enemies = FileJSON(Path.joinpath(HOME_DIR, "configs/enemies.json"))
json_maps = FileJSON(Path.joinpath(HOME_DIR, "configs/maps.json"))
sprites_loader = ImageLoader()

unit_types = {}
enemy_types = {}

screen = pygame.display.set_mode(SCREEN_SIZE)
coins = 0
wave = 1
shop = None
