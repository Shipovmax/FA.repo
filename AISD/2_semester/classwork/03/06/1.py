class Employee:

    def __init__(self, last_name, first_name, job_title, salary):

        self.last_name = last_name
        self.first_name = first_name
        self.job_title = job_title # Должность
        self.salary = salary
        self._experience = 0  # Стаж

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if value < 0:
            print("Стаж не может быть отрицательным!")
        else:
            self._experience = value

    def is_high_salary(self):
        if self.salary > 100000:
            return "Зарплата высокая (больше 100 000 рублей)"
        return "Зарплата обычная (100 000 рублей или меньше)"

    def __str__(self):
        return (f"Сотрудник: {self.last_name} {self.first_name}\n"
                f"Должность: {self.job_title}\n"
                f"Зарплата: {self.salary} руб.\n"
                f"Стаж: {self.experience} лет")

emp = Employee("Иванов", "Иван", "Разработчик", 120000)
emp.experience = 5
print(emp)
print(emp.is_high_salary())