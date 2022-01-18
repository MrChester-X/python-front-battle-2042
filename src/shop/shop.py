from globals.main_globals import coins, enemy_types, shop


class Shop:
    def __init__(self):
        pass

    '''
    Получить полный список всех товаров в магазине
    Возвращается список типов юнитов
    '''
    def get_all_items(self):
        return enemy_types

    '''
    Проверка, может ли игрок позволить себе этот товар
    В качестве 'enemy_type' выступает тип юнита
    '''
    def is_can_buy(self, enemy_type):
        return coins >= enemy_type.cost


def load_shop():
    shop = Shop()
