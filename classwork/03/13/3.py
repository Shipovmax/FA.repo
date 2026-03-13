from datetime import datetime


class Company:
    """Класс для представления строительной компании."""

    def __init__(self, name):
        self.name = name
        self.employees = []  # Список сотрудников компании

    def add_employee(self, worker):
        """Добавляет рабочего в штат компании и связывает рабочего с этой компанией."""
        self.employees.append(worker)
        worker.company = self

    def __str__(self):
        return f"Компания '{self.name}' (сотрудников: {len(self.employees)})"


class Worker:
    """Класс для описания рабочего."""

    def __init__(self, name, qualification, company=None):
        self.name = name
        self.qualification = qualification
        self.company = company
        # Если при создании указана компания, автоматически записываем в неё рабочего
        if company:
            company.add_employee(self)

    def __str__(self):
        # Если компания не задана, выводим 'Самозанятый'
        comp_name = self.company.name if self.company else "Самозанятый"
        return f"{self.name} ({self.qualification}) — {comp_name}"


class House:
    """Класс для описания строительного объекта (дома)."""

    def __init__(self, address, floors, entrances, district, workers, start_date_str, end_date_str):
        self.address = address
        self.floors = floors
        self.entrances = entrances
        self.district = district
        self.workers = workers  # Список рабочих, закрепленных за объектом

        # Преобразуем строки с датами в объекты datetime для удобного сравнения
        self.start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        self.end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

    def is_worker_busy_in_year(self, worker, year):
        """Проверяет, работал ли конкретный рабочий на этом объекте в указанном году."""
        # 1. Проверяем, числится ли вообще рабочий в списке этого дома
        if worker not in self.workers:
            return False

        # 2. Определяем границы искомого года
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)

        # 3. Логика пересечения интервалов:
        return self.start_date <= year_end and self.end_date >= year_start

    def __str__(self):
        return f"Объект в р-не {self.district} ({self.address}, {self.floors} этажей, {self.entrances} подъездов)"


class Registry:
    """Класс-реестр для хранения всех данных и вывода отчетов."""

    def __init__(self):
        self.houses = []
        self.workers = []

    def add_house(self, house):
        self.houses.append(house)

    def add_worker(self, worker):
        self.workers.append(worker)

    def show_worker_statistics(self, year):
        """Формирует и печатает отчет о занятости всех рабочих за конкретный год."""
        print(f"\n--- Отчет по занятости рабочих за {year} год ---")
        for worker in self.workers:
            # Ищем все дома, где этот рабочий был занят в указанном году
            projects = [h for h in self.houses if h.is_worker_busy_in_year(worker, year)]
            count = len(projects)

            if count > 0:
                print(f" {worker.name}: задействован в {count} проектах одновременно.")
                for p in projects:
                    print(f"   - {p}")
            else:
                print(f" {worker.name}: в этом году проектов не было.")


# --- Основной блок программы ---
if __name__ == "__main__":
    # Создаем компании
    stroy = Company("СтройГрупп")
    mega = Company("МегаДом")

    # Создаем рабочих и привязываем их к компаниям
    w1 = Worker("Иванов", "Бригадир", stroy)
    w2 = Worker("Петров", "Маляр", stroy)
    w3 = Worker("Сидоров", "Электрик", mega)

    # Инициализируем реестр и наполняем его данными
    registry = Registry()
    registry.add_worker(w1)
    registry.add_worker(w2)
    registry.add_worker(w3)

    # Добавляем объекты строительства с разными сроками
    registry.add_house(House("ул. Ленина, 10", 5, 4, "Центральный", [w1, w2], "01.01.2022", "31.12.2022"))
    registry.add_house(House("пр. Мира, 5", 9, 2, "Западный", [w1, w3], "01.06.2022", "01.06.2023"))
    registry.add_house(House("ул. Северная, 2", 16, 1, "Северный", [w1], "01.01.2023", "01.12.2023"))

    # Интерактивная часть: запрашиваем год у пользователя
    try:
        user_year = int(input("Введите год для проверки статистики (например, 2022): "))
        registry.show_worker_statistics(user_year)
    except ValueError:
        print("Ошибка: пожалуйста, введите число (год).")