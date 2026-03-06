class MushroomsCollector:
    def __init__(self):
        # Создаем список для каждого конкретного экземпляра (корзины)
        self.mushrooms = []

    def is_poisonous(self, mushroom_name):
        # Ошибка была в условии: 'Поганка' сама по себе всегда True.
        # Правильно проверять вхождение в список/кортеж:
        if mushroom_name in ("Мухомор", "Поганка"):
            return True
        return False

    def add_mushroom(self, mushroom_name):
        if not self.is_poisonous(mushroom_name):
            self.mushrooms.append(mushroom_name)
        else:
            print("Нельзя добавить ядовитый гриб")

    def __str__(self):
        # Соединяем элементы списка через запятую и пробел
        return ", ".join(self.mushrooms)


# Пример запуска
collector_1 = MushroomsCollector()
collector_1.add_mushroom("Мухомор")
collector_1.add_mushroom("Подосиновик")
collector_1.add_mushroom("Белый")
print(collector_1)

collector_2 = MushroomsCollector()
collector_2.add_mushroom("Лисичка")
print(collector_1)
print(collector_2)
