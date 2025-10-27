import re
import operator

# Словарь для чисел от 0 до 99
NUMBER_WORDS = {
    "ноль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
}

# Арифметические операции
OPERATIONS = {
    "плюс": operator.add,
    "минус": operator.sub,
    "умножить": operator.mul,
    "разделить": operator.truediv,
}

# Обратное отображение для преобразования чисел в слова
REVERSE_WORDS = {v: k for k, v in NUMBER_WORDS.items()}


def words_to_number(text):
    """Преобразует русские числительные в числовое значение"""
    if not text or text.strip() == "":
        raise ValueError("Пустое число")

    text = text.strip().lower()

    # Сначала обрабатываем простые числа
    if text in NUMBER_WORDS:
        return NUMBER_WORDS[text]

    # Обрабатываем составные числа типа "двадцать пять"
    words = text.split()
    total = 0

    for word in words:
        if word in NUMBER_WORDS:
            value = NUMBER_WORDS[word]
            if value >= 20:  # Это слово обозначает десятки
                total += value
            else:  # Это слово обозначает единицы
                total += value
        else:
            raise ValueError(f"Неизвестное слово: {word}")

    return total


def number_to_words(number):
    """Преобразует число в русские слова"""
    if number == 0:
        return "ноль"

    if number < 0:
        return "минус " + number_to_words(abs(number))

    # Обрабатываем числа, которые есть в словаре
    if number in REVERSE_WORDS:
        return REVERSE_WORDS[number]

    # Обрабатываем составные числа
    tens = (number // 10) * 10
    ones = number % 10

    if tens > 0 and ones > 0:
        return f"{REVERSE_WORDS[tens]} {REVERSE_WORDS[ones]}"
    elif tens > 0:
        return REVERSE_WORDS[tens]
    else:
        return REVERSE_WORDS[ones]


def parse_simple_expression(expression):
    """Разбирает простые выражения с двумя числами и одним оператором"""
    expression = expression.lower().strip()

    # Находим оператор
    found_operator = None
    operator_position = -1

    for op_word in OPERATIONS:
        if op_word in expression:
            found_operator = op_word
            operator_position = expression.find(op_word)
            break

    if not found_operator:
        raise ValueError("Оператор не найден в выражении")

    # Разделяем по позиции оператора
    left_text = expression[:operator_position].strip()
    right_text = expression[operator_position + len(found_operator) :].strip()

    # Для "умножить" и "разделить" удаляем слово "на" с правой стороны, если присутствует
    if found_operator in ["умножить", "разделить"]:
        right_text = re.sub(r"^на\s+", "", right_text)

    # Если правая часть пуста после очистки - это ошибка
    if not right_text:
        raise ValueError("Отсутствует второе число")

    # Преобразуем оба числа
    left_num = words_to_number(left_text)
    right_num = words_to_number(right_text)

    return left_num, found_operator, right_num


def calc(expression):
    """Главная функция калькулятора"""
    try:
        if not expression or expression.strip() == "":
            return "ошибка: пустое выражение"

        left_num, operator_word, right_num = parse_simple_expression(expression)
        operation = OPERATIONS[operator_word]

        # Проверяем деление на ноль
        if operator_word == "разделить" and right_num == 0:
            return "ошибка: деление на ноль"

        result = operation(left_num, right_num)

        # Обрабатываем числа с плавающей точкой
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                # Округляем до 2 знаков после запятой для простых случаев
                result = round(result, 2)

        return number_to_words(result)

    except ValueError as e:
        error_msg = str(e)
        if "Unknown word" in error_msg:
            unknown_word = error_msg.split(": ")[1]
            return f"ошибка: неизвестное слово '{unknown_word}'"
        elif "No operator" in error_msg:
            return "ошибка: не найден оператор (используйте плюс, минус, умножить, разделить)"
        elif "Missing right operand" in error_msg:
            return "ошибка: отсутствует второе число"
        elif "Empty number" in error_msg:
            return "ошибка: пустое число"
        else:
            return f"ошибка: {error_msg}"
    except Exception as e:
        return f"ошибка: неправильный формат выражения"


# Тестовые примеры
if __name__ == "__main__":
    print("=== Базовые тесты ===")
    print(calc("двадцать пять плюс тринадцать"))  # тридцать восемь
    print(calc("пять плюс три"))  # восемь
    print(calc("десять минус четыре"))  # шесть
    print(calc("шесть умножить на семь"))  # сорок два
    print(calc("шесть умножить семь"))  # сорок два (без "на")

    print("\n=== Тесты деления ===")
    print(calc("десять разделить на два"))  # пять
    print(calc("девять разделить на три"))  # три
    print(calc("десять разделить на ноль"))  # ошибка: деление на ноль
    print(calc("девять разделить три"))  # три (без "на")

    print("\n=== Тесты ошибок ===")
    print(calc("пять плюс"))  # ошибка: отсутствует второе число
    print(calc("разделить на пять"))  # ошибка: отсутствует первое число
    print(calc("пять плюс неизвестное"))  # ошибка: неизвестное слово 'неизвестное'
    print(calc(""))  # ошибка: пустое выражение