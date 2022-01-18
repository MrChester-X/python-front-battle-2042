import sys
from src.core.globals.main_globals import json_enemies, enemy_types


class EnemyType:
    def __init__(self, key):
        self.key = key
        self.load_json()

    def load_json(self):
        data = json_enemies.get_json()["enemies"]

        find = False
        for section in data:
            if section["key"] == self.key:
                data = section
                find = True
                break

        if not find:
            print(f"Не найден противник с ключом: {self.key}")
            sys.exit()

        self.name = data["name"]

        place_settings = data["place_settings"]

        self.sprite = place_settings["sprite"]
        self.radius_place = place_settings["radius_place"]

        skills = data["skills"]

        self.health = skills.get("health")
        self.speed = int(skills.get("speed")) / 2


def load_all_enemy_types():
    print("Загрузка противников...")
    data = json_enemies.get_json()["enemies"]

    for section in data:
        key = section["key"]
        enemy_types[key] = EnemyType(key)
        print(
            f"{enemy_types[key].key}: {enemy_types[key].name} (Здоровье: {enemy_types[key].health})")

    print("\033[92mВсе противники успешно загружены!\033[0m\n")
