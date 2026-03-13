class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender):
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender
        self.remaining_vacation_days = Employee.vacation_days
        self._employee_id = self.__generate_employee_id()

    def __generate_employee_id(self):
        return hash(self.first_name + self.second_name + self.gender)

    def consume_vacation(self, days):
        self.remaining_vacation_days -= days

    def get_vacation_details(self):
        return f'Остаток отпускных дней: {self.remaining_vacation_days}.'


class FullTimeEmployee(Employee):
    def __init__(self, first_name, second_name, gender, salary):
        super().__init__(first_name, second_name, gender)
        self.__salary = salary

    def __get_vacation_salary(self):
        return self.__salary * 0.8

    def get_unpaid_vacation(self, start_date, days):
        return f'Начало неоплачиваемого отпуска: {start_date}, продолжительность: {days} дней.'

    def get_vacation_salary_info(self):
        return f'Сумма отпускных: {self.__get_vacation_salary()}'


class PartTimeEmployee(Employee):
    pass


# Пример использования:

full_time_employee = FullTimeEmployee('Иван', 'Иванов', 'м', 50000)
print(f"ID сотрудника: {full_time_employee._employee_id}")
print(full_time_employee.get_unpaid_vacation('2023-07-01', 5))
print(full_time_employee.get_vacation_salary_info())

part_time_employee = PartTimeEmployee('Анна', 'Петрова', 'ж')
part_time_employee.consume_vacation(5)
print(f"ID сотрудника: {part_time_employee._employee_id}")
print(part_time_employee.get_vacation_details())
