#Clase que representa a un animal
class Animal:
   
    def __init__(self, nombre, edad, num_chip):
        self.__nombre = nombre
        self.__edad = edad
        self.num_chip = num_chip

    def sonido(self): #Método que simula el sonido del animal
        print("El animal hace un sonido")

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    def get_edad(self): # Método getter para acceder a la edad
        return self.__edad
    def set_edad(self, edad): # Método setter para modificar la edad
        if edad >= 0:
            self.__edad = edad
        else:
            self.__edad = 0
    
    def __str__(self): # Representación en cadena para el usuario
        return f"{self.__nombre} tiene {self.__edad} años y su identificación es: {self.num_chip}"
    
    def __eq__(self, other): # Comparación de igualdad entre objetos
        return self.num_chip == other.num_chip
    