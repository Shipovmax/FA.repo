import pytest

class Employee:
    """
    Класс Employee: представляет сотрудника компании и его данные.

    :param last_name: Фамилия сотрудника.
    :type last_name: str
    :param first_name: Имя сотрудника.
    :type first_name: str
    :param job_title: Должность сотрудника.
    :type job_title: str
    :param salary: Зарплата сотрудника в рублях.
    :type salary: int или float
    """

    def __init__(self, last_name, first_name, job_title, salary):
        """Инициализирует базовые атрибуты сотрудника."""
        self.last_name = last_name
        self.first_name = first_name
        self.job_title = job_title
        self.salary = salary
        self._experience = 0

    def experience_get(self):
        """
        Возвращает текущий стаж сотрудника.

        :return: Текущий стаж работы в годах.
        :rtype: int
        """
        return self._experience

    def experience_set(self, value):
        """
        Устанавливает стаж работы сотрудника с проверкой на отрицательные значения.

        :param value: Значение стажа для установки.
        :type value: int
        :raises ValueError: Если стаж отрицательный.
        """
        if value < 0:
            # Изменено на raise ValueError для корректной обработки ошибок
            raise ValueError("Стаж не может быть отрицательным!")
        self._experience = value

    def is_high_salary(self):
        """
        Проверяет уровень зарплаты сотрудника (порог 100 000 руб.).

        :return: Строка с оценкой уровня зарплаты.
        :rtype: str
        """
        if self.salary > 100000:
            return "Зарплата высокая (больше 100 000 рублей)"
        return "Зарплата обычная (100 000 рублей или меньше)"

    def __str__(self):
        """
        Возвращает форматированную строку с информацией о сотруднике.

        :return: Удобное для чтения строковое представление сотрудника.
        :rtype: str
        """
        return (f"Сотрудник: {self.last_name} {self.first_name}\n"
                f"Должность: {self.job_title}\n"
                f"Зарплата: {self.salary} руб.\n"
                f"Стаж: {self.experience} лет")

    experience = property(
        fget = experience_get,
        fset = experience_set,
        doc = "Свойство для безопасного доступа к стажу."
    )



# --- Блок тестов pytest ---

@pytest.fixture
def default_employee():
    """
    Фикстура pytest.
    Создает и возвращает стандартный объект сотрудника перед каждым тестом, 
    чтобы не дублировать код инициализации.
    """
    return Employee("Иванов", "Иван", "Разработчик", 120000)


help(Employee)


print("\n[ОПИСАНИЕ КЛАССА]")
print(Employee.__doc__.strip())


print("\n[КОНСТРУКТОР __init__]")
print(Employee.__init__.__doc__.strip())

print("\n[МЕТОД is_high_salary]")
print(Employee.is_high_salary.__doc__.strip())

print("\n[СВОЙСТВО experience]")
print(Employee.experience.__doc__.strip())

print("\n[ГЕТТЕР experience_get]")
print(Employee.experience_get.__doc__.strip())

print("\n[СЕТТЕР experience_set]")
print(Employee.experience_set.__doc__.strip())

print("\n[МЕТОД __str__]")
print(Employee.__str__.__doc__.strip())
print("\n=========================================")

