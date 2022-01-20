from src.core.globals.main_globals import enemy_types, sprites_loader
import pygame.sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()

        self.type = type

        self.dmg = 1

        self.load_health()
        self.load_sprite(pos)

        self.speed = enemy_types[self.type].speed

    def load_sprite(self, pos):
        self.image = sprites_loader.load_image(enemy_types[self.type].sprite)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def load_health(self):
        self.max_health = enemy_types[self.type].health
        self.health = self.max_health

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def attack(self, target):
        target.health -= self.dmg
