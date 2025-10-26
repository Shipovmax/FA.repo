# ---------- Библиотеки ----------

from __future__ import annotations
import re
from fractions import Fraction
from math import sin, cos, tan, pi, factorial
from typing import List, Tuple, Union, Optional

# ---------- Словари для преобразования слов <-> числа (русский) ----------

# Базовые числа
SIMPLE_NUM = {
    "ноль": 0,
    "один": 1,
    "одна": 1,
    "два": 2,
    "две": 2,
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
}

TENS = {
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
}

HUNDREDS = {
    "сто": 100,
    "двести": 200,
    "триста": 300,
    "четыреста": 400,
    "пятьсот": 500,
    "шестьсот": 600,
    "семьсот": 700,
    "восемьсот": 800,
    "девятьсот": 900,
}

# Разряды (тысячи, миллионы)
SCALES = {
    "тысяча": 10**3,
    "тысячи": 10**3,
    "тысяч": 10**3,
    "миллион": 10**6,
    "миллиона": 10**6,
    "миллионов": 10**6,
}

# Сопоставления для именования разрядов десятичной дроби
DECIMAL_DENOMINATORS = {
    "сотая": 100,
    "сотых": 100,
    "сотые": 100,
    "тысячная": 1000,
    "тысячных": 1000,
    "тысячные": 1000,
}

# Операторы (фразы) — все в нижнем регистре
OPERATORS = {
    "плюс": {"symbol": "+", "precedence": 1, "assoc": "left"},
    "минус": {"symbol": "-", "precedence": 1, "assoc": "left"},
    "умножить": {"symbol": "*", "precedence": 2, "assoc": "left"},
    "разделить": {"symbol": "/", "precedence": 2, "assoc": "left"},
    "остаток от деления": {"symbol": "%", "precedence": 2, "assoc": "left"},
    "в степени": {"symbol": "^", "precedence": 3, "assoc": "right"},
}

FUNCTIONS = {"синус", "косинус", "тангенс"}  # Функции (в виде ключевых слов)
COMBINATORICS = {
    "перестановок",
    "размещений",
    "сочетаний",
}  # Комбинаторные операции — будем распознавать по фразам

# Скобки — словесные формы
OPEN_PAREN = ("скобка открывается",)
CLOSE_PAREN = ("скобка закрывается",)

# Регулярные шаблоны для токенизации фраз
PHRASE_TOKENS = [
    "остаток от деления",
    "скобка открывается",
    "скобка закрывается",
    "в степени",
    "синус от",
    "косинус от",
    "тангенс от",
    "перестановок из",
    "размещений из",
    "сочетаний из",
    "плюс",
    "минус",
    "умножить",
    "разделить",
]


# ---------- Исключения / классы ошибок ----------
class CalcError(Exception):
    pass


class ParseError(CalcError):
    pass


class MathError(CalcError):
    pass


# ---------- Утилиты по работе с дробями и форматом вывода ----------
def fraction_to_decimal_with_period(
    fr: Fraction, max_nonrepeat: int = 10, max_period: int = 6
) -> Tuple[str, Optional[str]]:
    """
    Переводим дробь в десятичную запись с выделением периодической части.
    """

    # Анализируем знак
    sign = "-" if fr < 0 else ""
    fr = abs(fr)

    integer_part = fr.numerator // fr.denominator
    remainder = fr.numerator % fr.denominator

    if remainder == 0:
        return f"{sign}{integer_part}", None

    remainder_positions = {}
    decimals = []
    pos = 0
    repeating_start = None

    while remainder != 0 and pos < (max_nonrepeat + max_period + 5):
        if remainder in remainder_positions:
            repeating_start = remainder_positions[remainder]
            break
        remainder_positions[remainder] = pos
        remainder *= 10
        digit = remainder // fr.denominator
        decimals.append(str(digit))
        remainder %= fr.denominator
        pos += 1

    # Формируем части
    if repeating_start is None:
        dec_str = "".join(decimals)
        return (
            f"{sign}{integer_part}.{dec_str}",
            None,
        )  # нет периода в исследуемой длине — просто вернём неповторяющуюся дробь
    else:
        nonrep = "".join(decimals[:repeating_start])
        rep = "".join(decimals[repeating_start:])
        return (
            f"{sign}{integer_part}.{nonrep}" if nonrep else f"{sign}{integer_part}",
            rep,
        )


def fraction_to_mixed_and_words(fr: Fraction) -> str:
    """Возвращает строку на русском"""

    # Сохраняем знак
    sign_prefix = ""
    if fr < 0:
        sign_prefix = "минус "
        fr = abs(fr)

    # Целая часть
    entire_function = fr.numerator // fr.denominator
    fraction_function = Fraction(fr.numerator % fr.denominator, fr.denominator)

    parts = []
    if entire_function != 0:
        parts.append(int_to_words(entire_function))

    if fraction_function == 0:
        return (sign_prefix + parts[0]) if parts else sign_prefix + "ноль"

    # Сначала пробуем специальные разряды: сотые/тысячные/миллионные (100,1000,1000000)
    for denom_word, denom_value in [
        (100, "сотых"),
        (1000, "тысячных"),
        (10**6, "миллионных"),
    ]:

        if fraction_function.denominator == denom_value if False else False:
            pass  # оставлено для логики ниже

    # Если znaminatel_function делится на 2^a * 5^b => конечная десятичная fraction_function
    dec = None
    if is_terminating_decimal(fr):
        dec_str, period = fraction_to_decimal_with_period(
            fr, max_nonrepeat=10, max_period=6
        )
        if period is None:
            # разберём дробную часть
            if "." in dec_str:
                int_part_str, frac_part_str = dec_str.split(".", 1)
                length = len(frac_part_str)
                numerator = int(frac_part_str)
                if length in (2, 3, 6):
                    denom_map = {2: "сотых", 3: "тысячных", 6: "миллионных"}
                    denom_word = denom_map[length]

                    num_words = int_to_words(numerator)
                    if int(int_part_str) == 0:
                        return f"{sign_prefix}ноль и {num_words} {denom_word}"
                    else:
                        return f"{sign_prefix}{int_to_words(int(int_part_str))} и {num_words} {denom_word}"
                else:
                    rounded_frac = round(float(fr - int(fr)), 3)
                    rounded_frac_frac = Fraction(
                        str(round(fr - int(fr), 3))
                    ).limit_denominator()
                    if rounded_frac_frac == 0:
                        return f"{sign_prefix}{int_to_words(int(fr))}"
                    denom_try = {2: "сотых", 3: "тысячных"}
                    for l, word in denom_try.items():
                        numerator_try = int(round(fr - int(fr), l) * (10**l))
                        if abs(
                            (Fraction(numerator_try, 10**l) - (fr - int(fr)))
                        ) < Fraction(1, 10**l):
                            if int(fr) == 0:
                                return f"{sign_prefix}ноль и {int_to_words(numerator_try)} {word}"
                            else:
                                return f"{sign_prefix}{int_to_words(int(fr))} и {int_to_words(numerator_try)} {word}"
                    return sign_prefix + decimal_numeric_to_words(fr)
            else:
                return sign_prefix + int_to_words(int(dec_str))
        else:
            nonrep = dec_str.split(".", 1)[1] if "." in dec_str else ""
            if nonrep == "":
                nonrep_words = "ноль"
            else:
                nonrep_words = int_to_words(int(nonrep)) if nonrep != "" else "ноль"
            period_words = digits_to_words(period)
            if int(entire_function) == 0:
                return f"{sign_prefix}ноль и {nonrep_words} и {period_words} в периоде"
            else:
                return f"{sign_prefix}{int_to_words(entire_function)} и {nonrep_words} и {period_words} в периоде"
    else:
        # непериодическая бесконечная десятичная — будем пытаться обнаружить период (общий случай)
        dec_str, period = fraction_to_decimal_with_period(
            fr, max_nonrepeat=10, max_period=6
        )
        if period:
            # конвертируем в требуемую форму (ограничиваем период до 4 знаков в выводе)
            period_trimmed = period[:4]
            nonrep = dec_str.split(".", 1)[1] if "." in dec_str else ""
            nonrep_words = int_to_words(int(nonrep)) if nonrep else "ноль"
            period_words = digits_to_words(period_trimmed)
            if entire_function == 0:
                return f"{sign_prefix}ноль и {nonrep_words} и {period_words} в периоде"
            else:
                return f"{sign_prefix}{int_to_words(entire_function)} и {nonrep_words} и {period_words} в периоде"

    # Если дошли сюда — представим как смешанную fraction_function (entire_function и numerator_function/znaminatel_function)
    numerator_function = fraction_function.numerator
    znaminatel_function = fraction_function.denominator
    abbreviation_function = Fraction(
        numerator_function, znaminatel_function
    )  # уже сокращено
    if entire_function == 0:
        return f"{sign_prefix}{fraction_to_words(abbreviation_function)}"
    else:
        return f"{sign_prefix}{int_to_words(entire_function)} и {fraction_to_words(abbreviation_function)}"


def decimal_numeric_to_words(fr: Fraction) -> str:
    """
    Преобразует дробь в вид 'целая и X сотых/тысячных' если возможно, иначе в 'целая дробь' словами.
    """
    # попробуем округлить до тысячных и вывести
    val = float(fr)
    integer_part = int(val)
    frac_part = round(val - integer_part, 3)
    if frac_part == 0:
        return int_to_words(integer_part)
    digits3 = int(round(frac_part * 1000))
    if integer_part == 0:
        return f"ноль и {int_to_words(digits3)} тысячных"
    else:
        return f"{int_to_words(integer_part)} и {int_to_words(digits3)} тысячных"


def is_terminating_decimal(fr: Fraction) -> bool:
    """Проверяет, является ли дробь конечной десятичной (знаменатель содержит только 2 и 5)"""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def digits_to_words(digits: str) -> str:
    """
    Интерпретируем строку как число без ведущих нулей.
    """
    if digits == "":
        return "ноль"
    num = int(digits)
    return int_to_words(num)


def fraction_to_words(fr: Fraction) -> str:
    """
    Преобразует простую дробь (числитель/знаменатель, правильную) в текст
    """
    num = fr.numerator
    den = fr.denominator
    den_word = f"{ordinal_name_for_denominator(den)}"
    return f"{int_to_words(num)} {den_word}"


def ordinal_name_for_denominator(den: int) -> str:
    """
    Возвращает слово-форму для знаменателя в родительном/мн.ч. ('третьих', 'пятых')
    """
    if den == 2:
        return "вторых"
    if den == 3:
        return "третьих"
    if den == 4:
        return "четвертых"
    if den == 5:
        return "пятых"
    if den == 7:
        return "седьмых"
    if den == 9:
        return "девятых"
    # общая форма
    return f"{int_to_words(den)}-ых"


# ---------- Преобразование целого числа в слова (русский) ----------
# Поддержка до миллионов (потребуется для вывода больших результатов)
ONES = {
    0: "ноль",
    1: "один",
    2: "два",
    3: "три",
    4: "четыре",
    5: "пять",
    6: "шесть",
    7: "семь",
    8: "восемь",
    9: "девять",
    10: "десять",
    11: "одиннадцать",
    12: "двенадцать",
    13: "тринадцать",
    14: "четырнадцать",
    15: "пятнадцать",
    16: "шестнадцать",
    17: "семнадцать",
    18: "восемнадцать",
    19: "девятнадцать",
}
TENS_WORDS = {
    20: "двадцать",
    30: "тридцать",
    40: "сорок",
    50: "пятьдесят",
    60: "шестьдесят",
    70: "семьдесят",
    80: "восемьдесят",
    90: "девяносто",
}
HUND_WORDS = {
    100: "сто",
    200: "двести",
    300: "триста",
    400: "четыреста",
    500: "пятьсот",
    600: "шестьсот",
    700: "семьсот",
    800: "восемьсот",
    900: "девятьсот",
}


def int_to_words(n: int) -> str:
    """Преобразует неотрицательное целое число (до 999999) в русские слова."""
    if n == 0:
        return "ноль"
    if n < 0:
        return "минус " + int_to_words(-n)
    parts = []
    if n >= 10**6:
        millions = n // 10**6
        parts.append(
            int_to_words(millions)
            + " миллион"
            + ("ов" if millions % 10 != 1 or millions % 100 == 11 else "")
        )
        n %= 10**6
    if n >= 1000:
        thousands = n // 1000
        parts.append(_hundreds_to_words(thousands) + " " + _plural_thousand(thousands))
        n %= 1000
    if n > 0:
        parts.append(_hundreds_to_words(n))
    return " ".join([p for p in parts if p]).strip()


def _plural_thousand(n: int) -> str:
    """Правильное окончание для тысячи (упрощённо)"""
    if 11 <= (n % 100) <= 14:
        return "тысяч"
    last = n % 10
    if last == 1:
        return "тысяча"
    if 2 <= last <= 4:
        return "тысячи"
    return "тысяч"


def _hundreds_to_words(n: int) -> str:
    """Число до 999 в слова"""
    parts = []
    if n >= 100:
        h = (n // 100) * 100
        parts.append(HUND_WORDS.get(h, ""))
        n %= 100
    if n >= 20:
        t = (n // 10) * 10
        parts.append(TENS_WORDS.get(t, ""))
        n %= 10
    if n > 0:
        parts.append(ONES.get(n, ""))
    return " ".join([p for p in parts if p]).strip()


# ---------- Парсер слов в число ----------
def parse_simple_number_words(
    tokens: List[str], start_index: int = 0
) -> Tuple[int, int]:
    """
    Парсит последовательность слов, представляющих целое число (включая сотни, тысячи, миллионы).
    Возвращает (значение, индекс_последнего_слова_в_последовательности).
    Бросает ParseError при неизвестных словах.
    """
    i = start_index
    total = 0
    current = 0
    consumed = 0
    length = len(tokens)
    while i < length:
        w = tokens[i]
        if w in SIMPLE_NUM:
            current += SIMPLE_NUM[w]
            i += 1
            consumed += 1
        elif w in TENS:
            current += TENS[w]
            i += 1
            consumed += 1
        elif w in HUNDREDS:
            current += HUNDREDS[w]
            i += 1
            consumed += 1
        elif w in SCALES:
            scale = SCALES[w]
            if current == 0:
                current = 1
            total += current * scale
            current = 0
            i += 1
            consumed += 1
        else:
            break
    total += current
    if consumed == 0:
        raise ParseError(f"Ожидалось число, но найдено: '{tokens[start_index]}'")
    return total, start_index + consumed - 1


def parse_fractional_descriptor(
    tokens: List[str], start_index: int
) -> Tuple[Fraction, int]:
    """
    Парсит дробную часть, начиная с индекс start_index.
    Возвращает (Fraction, last_index).
    Бросает ParseError при некорректности.
    """
    # Попытаемся найти число (числитель)
    num, idx_num_end = parse_simple_number_words(tokens, start_index)
    # следующий токен — ожидаемо слово-разряд (сотая/тысячная) или форма 'третий/третьих' (упрощённо — мы ищем слово "сотая" или "тысячная" или любое слово, не число)
    next_idx = idx_num_end + 1
    if next_idx >= len(tokens):
        raise ParseError(
            "Ожидается слово-разряд (сотая/тысячная) после числителя дроби"
        )
    denom_word = tokens[next_idx]
    # Если это стандартная десятичная разрядность
    if denom_word in DECIMAL_DENOMINATORS:
        denom = DECIMAL_DENOMINATORS[denom_word]
        return Fraction(num, denom), next_idx
    else:
        base = denom_word
        if base in SIMPLE_NUM:
            denom = SIMPLE_NUM[base]
            return Fraction(num, denom), next_idx
        # Попытаемся убрать окончания
        for ending in ("ых", "ая", "ых", "ое", "ых", "их", "ых", "ых"):
            if base.endswith(ending):
                candidate = base[: -len(ending)]
                if candidate in SIMPLE_NUM:
                    denom = SIMPLE_NUM[candidate]
                    return Fraction(num, denom), next_idx
        # В противном случае — не поддерживаем такую форму
        raise ParseError(f"Неизвестный тип дробной части: '{denom_word}'")


def parse_mixed_or_decimal_number(
    tokens: List[str], start_index: int
) -> Tuple[Fraction, int]:
    """
    Парсит число, которое может быть: целым, смешанным, десятичной дробью
    """
    # Сначала пробуем целое
    val_int, idx_int_end = parse_simple_number_words(tokens, start_index)
    next_idx = idx_int_end + 1
    if next_idx < len(tokens) and tokens[next_idx] == "и":
        # есть дробная часть
        frac, idx_frac_end = parse_fractional_descriptor(tokens, next_idx + 1)
        return Fraction(val_int) + frac, idx_frac_end
    else:
        return Fraction(val_int), idx_int_end


# ---------- Токенизация входной строки ----------
def tokenize_expression(expr: str) -> List[Tuple[str, str]]:
    """
    Преобразует многословные операторы (например, "остаток от деления") в один токен.
    """
    s = expr.lower()
    # Удаляем лишние пробелы
    s = re.sub(r"\s+", " ", s).strip()
    tokens_raw = []
    i = 0
    words = s.split(" ")
    n = len(words)
    # Обходим список слов, пытаясь на каждом шаге найти многословную фразу из PHRASE_TOKENS
    while i < n:
        matched = False
        # Проверяем фразы в порядке убывания длины
        for phrase in PHRASE_TOKENS:
            phrase_parts = phrase.split(" ")
            lp = len(phrase_parts)
            if i + lp - 1 < n and words[i : i + lp] == phrase_parts:
                # распознали фразу
                tokens_raw.append(("PHRASE", phrase))
                i += lp
                matched = True
                break
        if matched:
            continue
        # Проверки для функций, у которых форма "синус от"
        if (
            i + 1 < n
            and words[i] in {"синус", "косинус", "тангенс"}
            and words[i + 1] == "от"
        ):
            tokens_raw.append(("PHRASE", words[i] + " от"))
            i += 2
            continue
        # Скобки словесные
        if i + 2 < n and words[i] == "скобка" and words[i + 1] == "открывается":
            tokens_raw.append(("PHRASE", "скобка открывается"))
            i += 2
            continue
        if i + 2 < n and words[i] == "скобка" and words[i + 1] == "закрывается":
            tokens_raw.append(("PHRASE", "скобка закрывается"))
            i += 2
            continue
        # Комбинаторика может быть двух/трёхсловной (например "размещений из")
        if i + 1 < n and words[i] in COMBINATORICS and words[i + 1] == "из":
            tokens_raw.append(("PHRASE", words[i] + " из"))
            i += 2
            continue
        # иначе — просто слово
        tokens_raw.append(("WORD", words[i]))
        i += 1

    # Свёртка фраз в операторы, функции и скобки
    tokens: List[Tuple[str, str]] = []
    for typ, val in tokens_raw:
        if typ == "PHRASE":
            if val in OPERATORS:
                tokens.append(("OP", OPERATORS[val]["symbol"]))
            elif val in OPEN_PAREN:
                tokens.append(("LPAREN", "("))
            elif val in CLOSE_PAREN:
                tokens.append(("RPAREN", ")"))
            elif val in ("синус от", "косинус от", "тангенс от"):
                func_name = val.split()[0]
                tokens.append(("FUNC", func_name))
            elif val.endswith(" из"):  # комбинаторика
                comb_kind = val.split()[0]  # 'перестановок'/'размещений'/'сочетаний'
                tokens.append(("COMB", comb_kind))
            elif val == "в степени":
                tokens.append(("OP", "^"))
            elif val == "остаток от деления":
                tokens.append(("OP", "%"))
            else:
                # другой оператор, например 'плюс', 'минус', 'умножить', 'разделить'
                if val in OPERATORS:
                    tokens.append(("OP", OPERATORS[val]["symbol"]))
                else:
                    tokens.append(("WORD", val))
        else:
            tokens.append((typ, val))
    return tokens


# ---------- Построение выражения в ОПЗ и парсинг чисел ----------
def shunting_yard_with_numbers(
    tokens: List[Tuple[str, str]],
) -> List[Tuple[str, Union[str, Fraction]]]:
    """
    Преобразует токены в обратную польскую запись (RPN), одновременно собирая числа.
    Возвращает список RPN-элементов: ('NUM', Fraction) или ('OP', symbol) или ('FUNC', name) или ('COMB', name)
    """
    output_queue: List[Tuple[str, Union[str, Fraction]]] = []
    operator_stack: List[Tuple[str, str]] = []

    # Преобразуем поток токенов в числовой поток
    i = 0
    length = len(tokens)

    while i < length:
        tok_type, tok_val = tokens[i]
        if tok_type == "WORD":
            # Собираем последовательность слов, относящуюся к числу
            j = i
            word_seq = []
            while j < length and tokens[j][0] == "WORD":
                word_seq.append(tokens[j][1])
                # заранее останавливаем, если следующими идут операторы/функции/скобки/COMB
                j += 1
            # Попробуем распознать число начиная от i:
            try:
                num, last_idx = parse_mixed_or_decimal_number([w for w in word_seq], 0)
                consumed = last_idx + 1
                output_queue.append(("NUM", num))
                i += consumed
                continue
            except ParseError as e:
                # Но если слово не оператор — выдаём ошибку
                if tok_val in {"плюс", "минус", "умножить", "разделить"}:
                    # не должно случаться — эти слова обычно распарсены ранее как PHRASE->OP
                    output_queue.append(("OP", OPERATORS[tok_val]["symbol"]))
                    i += 1
                    continue
                else:
                    raise ParseError(
                        f"Не удалось распознать число из слов: {' '.join(word_seq[:5])}... ({e})"
                    )
        elif tok_type == "NUM":
            output_queue.append(("NUM", tok_val))
            i += 1
        elif tok_type == "OP":
            op = tok_val
            # определяем precedence и assoc по символу
            prec, assoc = _operator_props(op)
            while operator_stack:
                top_type, top_val = operator_stack[-1]
                if top_type == "OP":
                    top_prec, _ = _operator_props(top_val)
                    if (assoc == "left" and prec <= top_prec) or (
                        assoc == "right" and prec < top_prec
                    ):
                        output_queue.append(("OP", top_val))
                        operator_stack.pop()
                        continue
                if top_type == "FUNC":
                    output_queue.append(("FUNC", top_val))
                    operator_stack.pop()
                    continue
                break
            operator_stack.append(("OP", op))
            i += 1
        elif tok_type == "FUNC":
            operator_stack.append(("FUNC", tok_val))
            i += 1
        elif tok_type == "COMB":
            # Комбинаторика — ожидаем далее числа: форма "перестановок из N" или "размещений из N по K"
            comb_kind = tok_val  # 'перестановок'/'размещений'/'сочетаний'
            j = i + 1
            # Сбор слов после COMB: пропускаем 'из' если есть
            if j < length and tokens[j][0] == "WORD" and tokens[j][1] == "из":
                j += 1
            # Соберём слова до оператора/скобки/COMB/FUNC
            word_seq = []
            k = j
            while k < length and tokens[k][0] == "WORD":
                # остановимся если получим 'по' — тогда следующая последовательность это K
                if tokens[k][1] == "по":
                    break
                word_seq.append(tokens[k][1])
                k += 1
            if not word_seq:
                raise ParseError(
                    "Ожидалось число после '... из' в комбинаторной операции"
                )
            n_val, _ = parse_mixed_or_decimal_number(word_seq, 0)
            # Теперь проверим есть ли 'по' и второе число
            if k < length and tokens[k][0] == "WORD" and tokens[k][1] == "по":
                # соберём слова после 'по'
                l = k + 1
                word_seq2 = []
                while l < length and tokens[l][0] == "WORD":
                    word_seq2.append(tokens[l][1])
                    l += 1
                if not word_seq2:
                    raise ParseError(
                        "Ожидалось число после 'по' в комбинаторной операции"
                    )
                k_val, _ = parse_mixed_or_decimal_number(word_seq2, 0)
                output_queue.append(("COMB", (comb_kind, n_val, k_val)))
                i = l
            else:
                output_queue.append(("COMB", (comb_kind, n_val, None)))
                i = k
        elif tok_type == "LPAREN":
            operator_stack.append(("LPAREN", tok_val))
            i += 1
        elif tok_type == "RPAREN":
            # выталкиваем до LPAREN
            found = False
            while operator_stack:
                top_type, top_val = operator_stack.pop()
                if top_type == "LPAREN":
                    found = True
                    break
                else:
                    output_queue.append((top_type, top_val))
            if not found:
                raise ParseError(
                    "Несбалансированные скобки (найдена закрывающая без открывающей)"
                )
            i += 1
        else:
            raise ParseError(f"Неизвестный тип токена: {tok_type}")
    while operator_stack:
        top_type, top_val = operator_stack.pop()
        if top_type in ("LPAREN", "RPAREN"):
            raise ParseError("Несбалансированные скобки (незакрытая скобка)")
        output_queue.append((top_type, top_val))
    return output_queue


def _operator_props(symbol: str) -> Tuple[int, str]:
    """Возвращает (precedence, assoc) для символа оператора"""
    for k, v in OPERATORS.items():
        if v["symbol"] == symbol:
            return v["precedence"], v["assoc"]
    if symbol == "^":
        return (3, "right")
    if symbol == "*":
        return (2, "left")
    if symbol == "/":
        return (2, "left")
    if symbol == "+":
        return (1, "left")
    if symbol == "-":
        return (1, "left")
    if symbol == "%":
        return (2, "left")
    # fallback
    return (1, "left")


# ---------- Оценщик выражения (вычисление RPN) ----------
def evaluate_rpn(rpn: List[Tuple[str, Union[str, Fraction]]]) -> Fraction:
    """
    Вычисляет выражение в обратной польской нотации.
    """
    stack: List[Fraction] = []
    for elem_type, elem_val in rpn:
        if elem_type == "NUM":
            stack.append(elem_val)
        elif elem_type == "OP":
            if len(stack) < 2:
                raise ParseError("Недостаточно операндов для бинарной операции")
            b = stack.pop()
            a = stack.pop()
            if elem_val == "+":
                stack.append(a + b)
            elif elem_val == "-":
                stack.append(a - b)
            elif elem_val == "*":
                stack.append(a * b)
            elif elem_val == "/":
                if b == 0:
                    raise MathError("Деление на ноль")
                stack.append(a / b)
            elif elem_val == "%":
                if b == 0:
                    raise MathError("Деление на ноль для операции остатка")
                quotient_floor = a // b
                stack.append(a - b * quotient_floor)
            elif elem_val == "^":
                if b.denominator != 1:
                    # нецелая степень — используем float
                    val = float(a) ** float(b)
                    stack.append(Fraction(val).limit_denominator(10**6))
                else:
                    exp = b.numerator
                    # поддержка отрицательных степеней
                    if exp >= 0:
                        stack.append(a**exp)
                    else:
                        # отрицательная целая степень
                        stack.append(Fraction(1, 1) / (a ** abs(exp)))
            else:
                raise ParseError(f"Неизвестный оператор '{elem_val}'")
        elif elem_type == "FUNC":
            # применяем функцию к верхнему элементу стека
            if len(stack) < 1:
                raise ParseError("Недостаточно операндов для функции")
            arg = stack.pop()
            # вычисляем тригонометрию в радианах: arg задаётся в радианах (если пользователь хочет градусы — нужно дополнительно)
            if elem_val == "синус":
                val = sin(float(arg))
                stack.append(Fraction(val).limit_denominator(10**6))
            elif elem_val == "косинус":
                val = cos(float(arg))
                stack.append(Fraction(val).limit_denominator(10**6))
            elif elem_val == "тангенс":
                val = tan(float(arg))
                stack.append(Fraction(val).limit_denominator(10**6))
            else:
                raise ParseError(f"Неизвестная функция '{elem_val}'")
        elif elem_type == "COMB":
            kind, n_val, k_val = elem_val
            # оба n_val и k_val — Fraction; ожидаем целые
            n = int(n_val)
            if k_val is None:
                if n < 0:
                    raise MathError("n для перестановок должен быть неотрицательным")
                result = factorial(n)
                stack.append(Fraction(result))
            else:
                k = int(k_val)
                if kind == "перестановок":
                    if k > n or n < 0 or k < 0:
                        stack.append(Fraction(0))
                    else:
                        result = factorial(n) // factorial(n - k)
                        stack.append(Fraction(result))
                elif kind == "размещений":
                    if k > n or n < 0 or k < 0:
                        stack.append(Fraction(0))
                    else:
                        result = factorial(n) // factorial(n - k)
                        stack.append(Fraction(result))
                elif kind == "сочетаний":
                    if k > n or n < 0 or k < 0:
                        stack.append(Fraction(0))
                    else:
                        result = factorial(n) // (factorial(k) * factorial(n - k))
                        stack.append(Fraction(result))
                else:
                    raise ParseError(f"Неизвестный вид комбинаторики: {kind}")
        else:
            raise ParseError(f"Неподдерживаемый элемент RPN: {elem_type}")
    if len(stack) != 1:
        raise ParseError(
            "Некорректное выражение (после вычисления остаётся более одного значения на стеке)"
        )
    return stack[0]


# ---------- Высокоуровневая функция calc ----------
def calc(expression: str) -> str:
    """
    Вход: строка-выражение на русском языке.
    Выход: строка с текстовым представлением результата.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ParseError("Пустая строка. Ожидается выражение.")

    # Нормализация и замены для удобства: 'пи' -> numeric token
    expr = expression.lower()
    expr = expr.replace("π", "пи")
    # Выполним токенизацию
    tokens = tokenize_expression(expr)

    # На стадии токенов обработаем простые случаи 'пи' как WORD -> заменим на NUM
    tokens_transformed: List[Tuple[str, str]] = []
    i = 0
    while i < len(tokens):
        ttype, tval = tokens[i]
        if ttype == "WORD" and tval == "пи":
            frac_pi = Fraction(str(pi)).limit_denominator(10**6)
            # вставляем специальный токен NUM (для последующей обработки)
            tokens_transformed.append(("NUM", frac_pi))
            i += 1
        else:
            tokens_transformed.append((ttype, tval))
            i += 1

    rpn_input = []
    for ttype, tval in tokens_transformed:
        if ttype == "NUM":
            rpn_input.append(("NUM", tval))
        else:
            rpn_input.append((ttype, tval))

    rpn = shunting_yard_with_numbers(rpn_input)

    # Вычисляем значение
    result_fraction = evaluate_rpn(rpn)

    # Форматируем результат в текст
    result_text = fraction_to_mixed_and_words(result_fraction)
    return result_text


print("Введите выражение:")
print(calc(str(input())))
