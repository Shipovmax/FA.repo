class Car:
    def __init__(self, marka, model , age , count):

        self.marka = marka
        self.model = model
        self.age = age
        self.count = count
        self.__tip = 'gasoline'

    def __str__(self):
        return f'марка {self.marka} модель {self.model} год производства {self.age} пробег брички {self.count}'

    def obs(self):
        if self.count > 10000:
            return 'нужно ТО'
        return 'не нужно ТО '

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, tip):
        self.__tip = tip

car_1 = Car('bmw' , 'x5m' , 2024 , 3000)
print(car_1)
print(car_1.obs())
print(car_1.tip)

