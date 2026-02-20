import math
from dataclasses import dataclass


@dataclass
class Triangle:
    side_a: float
    angle_beta: float
    angle_gamma: float

    def __post_init__(self) -> None:
        """Проверка корректности данных после создания объекта."""
        if self.side_a <= 0:
            raise ValueError("Длина стороны должна быть положительным числом.")
        if self.angle_beta <= 0 or self.angle_gamma <= 0:
            raise ValueError("Углы должны быть больше 0 градусов.")
        if self.angle_beta + self.angle_gamma >= 180:
            raise ValueError("Сумма двух углов должна быть меньше 180 градусов.")

    @property
    def angle_alpha(self) -> float:
        """Вычисляет третий угол (противолежащий стороне a)."""
        return 180 - (self.angle_beta + self.angle_gamma)

    @property
    def _radians(self) -> tuple[float, float, float]:
        """Внутренний метод для перевода всех углов в радианы."""
        return (
            math.radians(self.angle_alpha),
            math.radians(self.angle_beta),
            math.radians(self.angle_gamma)
        )

    @property
    def side_b(self) -> float:
        """Вычисляет сторону b по теореме синусов."""
        rad_a, rad_b, _ = self._radians
        return (self.side_a * math.sin(rad_b)) / math.sin(rad_a)

    @property
    def side_c(self) -> float:
        """Вычисляет сторону c по теореме синусов."""
        rad_a, _, rad_g = self._radians
        return (self.side_a * math.sin(rad_g)) / math.sin(rad_a)

    @property
    def triangle_type(self) -> str:
        """Определяет вид треугольника по углам и сторонам."""
        angles = sorted([self.angle_alpha, self.angle_beta, self.angle_gamma])

        # 1. Классификация по углам
        if any(math.isclose(a, 90) for a in angles):
            angle_kind = "прямоугольный"
        elif any(a > 90 for a in angles):
            angle_kind = "тупоугольный"
        else:
            angle_kind = "остроугольный"

        # 2. Классификация по сторонам (углам)
        if math.isclose(angles[0], angles[2]):
            return "равносторонний"  # Если все углы равны, дальше проверять нет смысла

        if math.isclose(angles[0], angles[1]) or math.isclose(angles[1], angles[2]):
            side_kind = "равнобедренный"
        else:
            side_kind = "разносторонний"

        # Исправленная f-строка (без лишних скобок)
        return f"{angle_kind}, {side_kind}"


# --- Блок тестирования ---
try:
    # Пример 1: Прямоугольный равнобедренный треугольник
    tri = Triangle(side_a=10, angle_beta=45, angle_gamma=45)

    print(f"Информация о фигуре: {tri}")
    print(f"Третий угол (alpha): {tri.angle_alpha}°")
    print(f"Стороны: b = {tri.side_b:.2f}, c = {tri.side_c:.2f}")
    print(f"Тип: {tri.triangle_type}")

    print("-" * 30)

    # Пример 2: Проверка ошибки
    # tri_error = Triangle(10, 90, 90)

except ValueError as e:
    print(f"Ошибка валидации: {e}")