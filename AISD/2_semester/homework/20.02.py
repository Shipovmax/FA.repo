'''Задача . Создайте класс Часы по переводу минут в часы или секунды.
Пользователь должен задать время, например, 89 минут, и также пользователь должен
определить в часы или в секунды перевести заданное время. Используйте
принципы абстракции, инкапсуляции, а также конструктор классов'''

class Clock:
    def __init__(self, minutes: int):
        self.__minutes = minutes

    def to_hours(self):
        return self.__minutes / 60

    def to_seconds(self):
        return self.__minutes * 60

# Тесты

minutes = int(input("Введите количество минут: "))
clock = Clock(minutes)

choice = input("Перевести в (часы/секунды): ").lower()

if choice == "часы":
    print("Часы:", clock.to_hours())
elif choice == "секунды":
    print("Секунды:", clock.to_seconds())
else:
    print("Неверный выбор")