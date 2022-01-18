from globals.main_globals import enemy_types


class Enemy:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        self.load_health()

    def load_health(self):
        self.max_health = enemy_types[self.type].health;
        self.health = self.max_health
