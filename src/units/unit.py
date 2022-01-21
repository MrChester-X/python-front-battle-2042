import pygame
from src.core.globals.main_globals import unit_types, sprites_loader, enemy_types


class Unit(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()

        self.type = type
        self.pos = pos

        self.load_sprite(pos)

    def load_sprite(self, pos):
        self.image = sprites_loader.load_image(unit_types[self.type].sprite)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
