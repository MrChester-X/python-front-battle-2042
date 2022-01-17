import pygame.sprite
from src.config.image_controller import ImageLoader
from src.config.json_controller import FileJSON
from pathlib import Path
import sys
import pprint


class BlankEnemy(pygame.sprite.Sprite):
    def __init__(self, key=''):
        super().__init__()

        self.key = key

        # Пока я эти данные в каждом файле буду обьявлять,
        # под конец работы вынесем в отдельный файл settings.json

        self.HOME_DIR = Path(__file__).resolve().parent.parent.parent
        self.CONFIG_DIR = Path.joinpath(self.HOME_DIR, 'configs')
        self.FPS = 60
        self.TILE_SIZE = 100

        try:
            self.json_controller = FileJSON(Path.joinpath(self.CONFIG_DIR, 'enemies.json'))
            stats = list(filter(
                lambda x: x['key'] == self.key, self.json_controller.get_json()['enemies']))[0]

            self.hp = stats['skills']['health']
            self.speed = int(stats['skills']['speed']) / 2
            self.name = stats['name']

            self.image = ImageLoader.load_image(stats['place_settings']['sprite'])

            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0

        except FileNotFoundError:
            print('Файла конфигурации не существует')
            sys.exit()
        except IndexError:
            print('Персонажа не существует')
            sys.exit()

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed


class Zombie(BlankEnemy):
    def __init__(self):
        self.key = 'zombie'
        super().__init__(self.key)


class FastZombie(BlankEnemy):
    def __init__(self):
        self.key = 'fast_zombie'
        super().__init__(self.key)
