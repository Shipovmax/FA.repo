class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        field = [['.' for _ in range(40)] for _ in range(40)]
        if 0 <= self.y < 40 and 0 <= self.x < 40:
            field[self.y][self.x] = '*'
        
        print('Поле 40x40:')
        for row in field:
            print(''.join(row))

# 2) Создание объекта фигуры
fig = Figure(5, 5)

# 4) Нарисовать фигуру
fig.draw()

# 5) Изменить параметры и перерисовать
fig.x = 20
fig.y = 15
fig.draw()
