import math
from dataclasses import dataclass


@dataclass
class Cone:
    radius: float
    height: float

    def __post_init__(self):
        """Проверка данных после инициализации объекта."""
        if self.radius <= 0 or self.height <= 0:
            raise ValueError("Радиус и высота должны быть больше нуля.")

    @property
    def slant_height(self) -> float:
        """Образующая конуса (l)."""
        return math.hypot(self.radius, self.height)

    @property
    def area(self) -> float:
        """Полная площадь поверхности."""
        return math.pi * self.radius * (self.radius + self.slant_height)

    @property
    def volume(self) -> float:
        """Объем конуса."""
        return (1 / 3) * math.pi * (self.radius ** 2) * self.height


try:
    cone = Cone(5, 12)
    print(cone)
    print(f"Площадь: {cone.area:.2f}")
    print(f"Объем: {cone.volume:.2f}")
    print(f"Образующая: {cone.slant_height:.2f}")

except ValueError as e:
    print(f"Ошибка: {e}")