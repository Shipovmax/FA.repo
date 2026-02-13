'''Задача . Создать класс Учитель и Ученик. По результатам работы данных классов
вывести на экран всех учеников, которых обучил учитель. Для каждого ученика вывести
информацию, по какому предмету они обучились и их оценку.'''

class Student:
    def __init__(self, name, subject, grade):
        self.name = name
        self.subject = subject
        self.grade = grade

    def get_info(self):
        return f"Ученик: {self.name}, предмет: {self.subject}, оценка: {self.grade}"


class Teacher:
    def __init__(self, name):
        self.name = name
        self.students = []

    def teach(self, student):
        """Добавить обученного ученика"""
        self.students.append(student)

    def show_students(self):
        print(f"Учитель {self.name} обучил следующих учеников:\n")

        if not self.students:
            print("Нет обученных учеников.")
            return

        for student in self.students:
            print(student.get_info())


# Тесты

teacher = Teacher("Иван Петров")

s1 = Student("Алексей", "Математика", 5)
s2 = Student("Мария", "Физика", 4)
s3 = Student("Дмитрий", "Информатика", 5)

teacher.teach(s1)
teacher.teach(s2)
teacher.teach(s3)

teacher.show_students()