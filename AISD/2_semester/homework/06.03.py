class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender):
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender
        self.remaining_vacation_days = self.vacation_days

    def consume_vacation(self, days):
        self.remaining_vacation_days -= days

    def get_vacation_details(self):
        return f"Остаток отпускных дней: {self.remaining_vacation_days}."


class FullTimeEmployee(Employee):
    def get_unpaid_vacation(self, start_date, days):
        return (
            f"Начало неоплачиваемого отпуска: {start_date}, "
            f"продолжительность: {days} дней."
        )


class PartTimeEmployee(Employee):
    # Переопределяем количество дней только для этого класса
    vacation_days = 14


# --- Пример использования ---

full_time = FullTimeEmployee("Роберт", "Крузо", "м")
print(f"Фултайм ({full_time.first_name}): {full_time.get_vacation_details()}")
print(full_time.get_unpaid_vacation("2023-07-01", 5))

print("-" * 30)

part_time = PartTimeEmployee("Алёна", "Пятницкая", "ж")
print(f"Парттайм ({part_time.first_name}): {part_time.get_vacation_details()}")