import random


class Team:
    """
    Родительский класс для всех тим
    """
    
    def __init__(self, name, country="Unknown"):
        self.name = name
        self.country = country
        self.rating = 0             # Рейтинг
        self.form = 1.0             # (ФОРМА) Коэффицент выносливости команды в течение матча (меняется динамично)
        self.tactics = ""           # Тактика (Будем рандомизировать для каждой тимы)
        self.wins = 0               # Победы
        self.losses = 0             # Поражения
    
    def calculate_power(self):
        """
        Рассчитать силу команды для матча
        """
        
        base_power = self.rating
        form_bonus = random.uniform(0.8, 1.2) * self.form
        return base_power * form_bonus
    
    def update_after_match(self, won=False):
        """
        Обновить статистику после матча
        """
        
        if won:
            self.wins += 1
            self.form = min(2.0, self.form + 0.1)  # Форма растет
        
        else:
            self.losses += 1  
            self.form = max(0.5, self.form - 0.1)  # Форма падает
    
    def __str__(self):
        return f"{self.name} | Рейтинг: {self.rating} | Форма: {self.form}"
    
    