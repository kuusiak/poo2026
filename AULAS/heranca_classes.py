class Animal:
    def __init__(self, nome, especie, patas):
        self.nome = nome
        self.especie = especie
        self.patas = patas

    def respirar(self):
        print("Respirando...")

    def rugir(self):
        print("RAWR")
    
class Cachorro(Animal):
    def abanarRabo(self):
        print("Abanar Rabo")

    def rugir(self):
        print("Au Au!")    

class Gato(Animal):
    def __init__(self, nome, especie, patas, dono):
        super().__init__(nome, especie, patas)
        self.dono = dono

    def ronronar(self):
        print("Ronronar")
    
    def rugir(self):
        print("Miau!") 