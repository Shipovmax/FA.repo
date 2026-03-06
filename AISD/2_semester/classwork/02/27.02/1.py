class BacteriaProducer:
    def __init__(self, max_bacteria):
        # Устанавливаем максимальный предел
        self.max_bacteria = max_bacteria
        # Текущее количество по умолчанию 0
        self.current_bacteria = 0

    def create_new(self):
        if self.current_bacteria < self.max_bacteria:
            self.current_bacteria += 1
            print(
                f"Добавлена одна бактерия. Количество бактерий в популяции: {self.current_bacteria}"
            )
        else:
            print("Нет места под новую бактерию")

    def remove_one(self):
        if self.current_bacteria > 0:
            self.current_bacteria -= 1
            print(
                f"Одна бактерия удалена. Количество бактерий в популяции: {self.current_bacteria}"
            )
        else:
            print("В популяции нет бактерий, удалять нечего")


# Пример запуска
bacteria_producer = BacteriaProducer(max_bacteria=3)
bacteria_producer.remove_one()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.remove_one()
