# ==================================================
# ЗАДАНИЕ 1
# ==================================================
# УСЛОВИЕ:
# Создать класс Car, который содержит следующие поля:
# - марка автомобиля
# - цвет автомобиля
# - максимальная скорость
#
# Создать два объекта данного класса и вывести их данные.
#
# РЕШЕНИЕ:
# ==================================================

class Car:
    def __init__(self, brand, color, max_speed):
        self.brand = brand
        self.color = color
        self.max_speed = max_speed


car1 = Car("BMW", "Black", 250)
car2 = Car("Audi", "White", 230)

print("Задание 1")
print(car1.brand, car1.color, car1.max_speed)
print(car2.brand, car2.color, car2.max_speed)
print()


# ==================================================
# ЗАДАНИЕ 2
# ==================================================
# УСЛОВИЕ:
# Для объектов класса Car добавить динамические атрибуты:
# - вес автомобиля
# - количество владельцев
#
# Вывести новые данные на экран.
#
# РЕШЕНИЕ:
# ==================================================

car1.weight = 1800
car1.owners = 2

car2.weight = 1650
car2.owners = 1

print("Задание 2")
print("Вес:", car1.weight, "Владельцы:", car1.owners)
print("Вес:", car2.weight, "Владельцы:", car2.owners)
print()


# ==================================================
# ЗАДАНИЕ 3
# ==================================================
# УСЛОВИЕ:
# В класс Car добавить методы:
# - вычисление общего веса
# - сравнение веса двух автомобилей
# - вывод полной информации
#
# Реализовать работу методов.
#
# РЕШЕНИЕ:
# ==================================================

class CarAdvanced:
    def __init__(self, brand, color, max_speed, weight, count):
        self.brand = brand
        self.color = color
        self.max_speed = max_speed
        self.weight = weight
        self.count = count

    def total_weight(self):
        return self.weight * self.count

    def compare(self, other):
        if self.total_weight() > other.total_weight():
            return "Первая машина тяжелее"
        elif self.total_weight() < other.total_weight():
            return "Вторая машина тяжелее"
        else:
            return "Вес одинаковый"

    def info(self):
        print("Марка:", self.brand)
        print("Цвет:", self.color)
        print("Скорость:", self.max_speed)
        print("Общий вес:", self.total_weight())
        print()


car3 = CarAdvanced("BMW", "Black", 250, 1800, 2)
car4 = CarAdvanced("Audi", "White", 230, 1600, 1)

print("Задание 3")
car3.info()
car4.info()
print(car3.compare(car4))
print()


# ==================================================
# ЗАДАНИЕ 4
# ==================================================
# УСЛОВИЕ:
# Создать класс Student со следующими полями:
# - имя
# - возраст
# - курс
# - средний балл
#
# Создать методы:
# - вывод информации
# - вывод среднего балла
#
# РЕШЕНИЕ:
# ==================================================

class Student:
    def __init__(self, name, age, course, grade):
        self.name = name
        self.age = age
        self.course = course
        self.grade = grade

    def show_grade(self):
        print("Средний балл:", self.grade)

    def info(self):
        print("Имя:", self.name)
        print("Возраст:", self.age)
        print("Курс:", self.course)
        print("Балл:", self.grade)
        print()


student = Student("Maxim", 19, 2, 4.5)

print("Задание 4")
student.info()
student.show_grade()
print()


# ==================================================
# ЗАДАНИЕ 5
# ==================================================
# УСЛОВИЕ:
# В класс Student добавить методы:
# - изменение имени
# - изменение возраста
# - изменение среднего балла
#
# Проверить работу методов.
#
# РЕШЕНИЕ:
# ==================================================

class StudentAdvanced(Student):
    def change_name(self, new_name):
        self.name = new_name

    def change_age(self, new_age):
        self.age = new_age

    def change_grade(self, new_grade):
        self.grade = new_grade


student2 = StudentAdvanced("Maxim", 19, 2, 4.5)

print("Задание 5")

student2.change_name("Alex")
student2.change_age(20)
student2.change_grade(4.9)

student2.info()
print()


# ==================================================
# ЗАДАНИЕ 6
# ==================================================
# УСЛОВИЕ:
# Создать класс Calculator, который принимает строку
# вида: "6 - 7 + 4"
#
# Реализовать вычисление выражения,
# используя операции + и -.
#
# РЕШЕНИЕ:
# ==================================================

class Calculator:

    def calculate(self, text):
        parts = text.split()

        result = int(parts[0])

        i = 1
        while i < len(parts):
            op = parts[i]
            num = int(parts[i + 1])

            if op == "+":
                result += num
            elif op == "-":
                result -= num

            i += 2

        return result


calc = Calculator()

example = "4 - 7 + 4"

print("Задание 6")
print("Пример:", example)
print("Результат:", calc.calculate(example))
print()
