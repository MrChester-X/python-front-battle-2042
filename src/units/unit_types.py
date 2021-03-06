import sys
from src.core.globals.main_globals import json_units, unit_types


class UnitType:
    def __init__(self, key):
        self.key = key
        self.load_json()

    def load_json(self):
        data = json_units.get_json()["units"]

        # Надо же найти этого юнита в конфиге =)

        find = False
        for section in data:
            if section["key"] == self.key:
                data = section
                find = True
                break

        if not find:
            print(f"Не найден юнит с ключом: {self.key}")
            sys.exit()

        self.name = data["name"]

        place_settings = data["place_settings"]

        self.sprite = place_settings["sprite"]
        self.cost = place_settings["cost"]
        self.radius_place = place_settings["radius_place"]

        skills = data["skills"]

        # В случае, если скилла нет, вернет None
        # От этого None будем оттакливаться в будущем (у каждого юнита свои скиллы)

        self.radius = skills.get("radius")
        self.damage = skills.get("damage")
        self.reload = skills.get("reload")


def load_all_unit_types():
    print("Загрузка юнитов...")
    data = json_units.get_json()["units"]

    for section in data:
        key = section["key"]
        unit_types[key] = UnitType(key)
        print(f"{unit_types[key].key}: {unit_types[key].name} (Цена: {unit_types[key].cost}$)")

    print("\033[92mВсе юниты успешно загружены!\033[0m\n")
