from config.json_controller import FileJSON

json_units = FileJSON("configs/units.json")
json_enemies = FileJSON("configs/enemies.json")
json_maps = FileJSON("configs/maps.json")

unit_types = {}
enemy_types = {}

coins = 0
shop = None
