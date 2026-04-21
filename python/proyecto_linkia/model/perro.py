from model.animal import Animal


class Perro(Animal):
   
    def __init__(self, nombre, edad, num_chip, ladrido):
        self.__nombre = nombre
        self.__edad = edad
        self.num_chip = num_chip
        self.ladrido = ladrido
