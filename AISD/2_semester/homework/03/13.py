class Student:
    """Базовый класс СТУДЕНТ"""
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def display_info(self):
        """Метод вывода информации (переопределяется в дочерних классах)"""
        return f"Студент: {self.first_name} {self.last_name}, Возраст: {self.age}"

    def matches_conditions(self, **kwargs):
        """
        Универсальный метод проверки соответствия условиям.
        Передаются именованные аргументы, например: age=20, course=3
        """
        for key, value in kwargs.items():
            # getattr возвращает значение атрибута объекта, если его нет — возвращает None
            if getattr(self, key, None) != value:
                return False
        return True


class Bachelor(Student):
    """Дочерний класс БАКАЛАВР"""
    def __init__(self, first_name, last_name, age, course):
        super().__init__(first_name, last_name, age)
        self.course = course

    def display_info(self):
        return f"[Бакалавр] {self.first_name} {self.last_name}, Возраст: {self.age}, Курс: {self.course}"


class Master(Student):
    """Дочерний класс МАГИСТР"""
    def __init__(self, first_name, last_name, age, specialization):
        super().__init__(first_name, last_name, age)
        self.specialization = specialization

    def display_info(self):
        return f"[Магистр] {self.first_name} {self.last_name}, Возраст: {self.age}, Спец-ть: {self.specialization}"


class Postgraduate(Student):
    """Дочерний класс АСПИРАНТ"""
    def __init__(self, first_name, last_name, age, thesis_topic):
        super().__init__(first_name, last_name, age)
        self.thesis_topic = thesis_topic

    def display_info(self):
        return f"[Аспирант] {self.first_name} {self.last_name}, Возраст: {self.age}, Тема диссертации: '{self.thesis_topic}'"



students_db = [
    Bachelor("Иван", "Иванов", 20, 3),
    Bachelor("Анна", "Петрова", 19, 2),
    Bachelor("Максим", "Сидоров", 20, 3),
    Master("Елена", "Смирнова", 23, "Программная инженерия"),
    Master("Алексей", "Волков", 24, "Анализ данных"),
    Postgraduate("Дмитрий", "Соколов", 26, "Оптимизация ИИ-моделей"),
    Postgraduate("Ольга", "Морозова", 25, "Информационная безопасность")
]

print("=== ПОЛНАЯ БАЗА СТУДЕНТОВ ===")
for student in students_db:
    print(student.display_info())
print("\n" + "="*30 + "\n")


def search_students(db, **conditions):
    """Вспомогательная функция для вывода результатов поиска"""
    print(f"--- Результаты поиска по условиям: {conditions} ---")
    found = False
    for student in db:
        if student.matches_conditions(**conditions):
            print(student.display_info())
            found = True
    if not found:
        print("Студенты, удовлетворяющие условиям, не найдены.")
    print()

search_students(students_db, age=20)
search_students(students_db, course=3)
search_students(students_db, specialization="Программная инженерия")
search_students(students_db, age=25, thesis_topic="Информационная безопасность")