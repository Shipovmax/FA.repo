class Student():
    def __init__(self, name , age , clas , srb):
        self.name = name
        self.age = age
        self.clas = clas
        self.srb = srb

    def izm_b(self, new_bal):
        self.srb = new_bal
        
    def bal(self):
        return self.srb
    
    def got(self):
        return (self.name, self.age , self.clas , self.srb)

    def __str__(self):
        return f'имя {self.name} возраст {self.age} класс {self.clas} балл {self.srb}'

student_1 = Student("Vasia" , 12 , "9B" , 4.5)
student_2 = Student("Ivan" , 14 , "11A" , 3.2)

print(student_1.__dict__)
student_1.izm_b(4.8)
print(student_1.bal())
print(student_1.got())
print(student_1)



