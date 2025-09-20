class Dog:
    def __init__(self,name,breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f'{self.name} is barking')

dog1 = Dog('Will','Labrodor')
dog2 = Dog('Luna','German Sheperd')

dog1.bark()
dog2.bark()