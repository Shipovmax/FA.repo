import time


class TuringMachine:
    def __init__(
        self, tape_string, transitions, initial_state="q0", final_states=None, blank="_"
    ):
        # Инициализируем ленту как словарь, где ключ - это индекс ячейки
        self.tape = {i: char for i, char in enumerate(tape_string)}
        self.transitions = transitions
        self.state = initial_state
        self.final_states = final_states if final_states else {"q_done"}
        self.blank = blank
        self.head = 0

    def step(self):
        """Выполняет ровно один шаг вычислений."""

        # Смотрим символ под головкой
        current_symbol = self.tape.get(self.head, self.blank)

        # Ищем правило в словаре переходов
        action = self.transitions.get((self.state, current_symbol))

        if not action:
            return False  # Если правила нет - аварийная остановка

        new_state, new_symbol, direction = action

        # 1. Записываем новый символ
        self.tape[self.head] = new_symbol

        # 2. Меняем состояние
        self.state = new_state

        # 3. Двигаем головку
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1

        return True

    def visualize(self, step_num):
        """Красиво выводит текущее состояние ленты и каретки в консоль."""

        keys = list(self.tape.keys())
        # Находим границы ленты (плюс по одной пустой ячейке по краям для красоты)
        min_pos = min(min(keys) if keys else 0, self.head) - 1
        max_pos = max(max(keys) if keys else 0, self.head) + 1

        tape_str = ""
        head_indicator = ""

        for i in range(min_pos, max_pos + 1):
            char = self.tape.get(i, self.blank)
            tape_str += f"[{char}]"

            # Ставим указатель ровно под текущей ячейкой
            if i == self.head:
                head_indicator += " ^ "
            else:
                head_indicator += "   "

        print(f"Шаг {step_num:02d} | Текущее состояние: {self.state}")
        print(f"Лента:   {tape_str}")
        print(f"Головка: {head_indicator}")
        print("-" * 40)

    def run(self, delay=0.5, max_steps=1000):
        """Главный цикл работы эмулятора."""

        step_num = 0
        self.visualize(step_num)

        while self.state not in self.final_states and step_num < max_steps:
            time.sleep(delay)  # Пауза, чтобы была видна анимация в консоли

            if not self.step():
                print("❌ ОШИБКА: Нет правила для текущей ситуации. Машина сломалась.")
                break

            step_num += 1
            self.visualize(step_num)

        if self.state in self.final_states:
            print(
                "✅ УСПЕХ: Машина достигла финального состояния и успешно остановилась."
            )


# ==========================================
# ВХОДНЫЕ ДАННЫЕ И ПРАВИЛА ПОВЕДЕНИЯ МАШИНЫ
# ==========================================

# Пример алгоритма: Инвертируем биты (0 меняем на 1, 1 на 0),
# и останавливаемся, когда дойдем до пустого символа '_'.
rules = {
    # (текущее_состояние, видим_символ): (новое_состояние, пишем_символ, куда_идем)
    ("q0", "0"): ("q0", "1", "R"),
    ("q0", "1"): ("q0", "0", "R"),
    ("q0", "_"): ("q_done", "_", "N"),  # N - стоим на месте (None/Neutral)
}

# Начальная строка на ленте
initial_tape = "100110"

# Создаем и запускаем машину
if __name__ == "__main__":
    print("🚀 Запуск эмулятора Машины Тьюринга...\n")
    tm = TuringMachine(tape_string=initial_tape, transitions=rules, initial_state="q0")

    # delay задает скорость анимации (в секундах)
    tm.run(delay=0.8)
