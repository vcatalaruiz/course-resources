


from model.animal import Animal
from model.perro import Perro


animal = Animal("Boby", 5, 1234) #0x393939393

animal2 = Animal("Boby", 5, 1234) #0x83838383

perro = Perro("Boby", 5, 1234, "Guau")
perro.sonido()

print(animal)

