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

    def __tip_get(self):
        return self.__tip

    def __tip_set(self, tip):
        self.__tip = tip

    def __tip_del(self):
        del self.__tip

    tip = property(fget= __tip_get(),fset= __tip_set(), fdel= __tip_del())

car_1 = Car('bmw' , 'x5m' , 2024 , 3000)
print(car_1)
print(car_1.obs())
print(car_1.tip_get())
print(car_1.tip_set('diesel'))
print(car_1.tip_del())

