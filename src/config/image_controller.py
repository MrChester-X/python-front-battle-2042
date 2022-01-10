import os
import sys
import pygame
from pathlib import Path


class ImageLoader:
    @staticmethod
    def load_image(name, colorkey=None):
        sprite_path = Path.joinpath(Path(__file__).resolve().parent.parent.parent, 'sprites')
        fullname = Path.joinpath(sprite_path, name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image
