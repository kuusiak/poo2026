import math
class Calculadora:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
    
    def somar(self, a, b):
        resultado = a + b
        return resultado
        
    def subtrair(self, a, b):
        resultado = a - b
        return resultado
        
    def multiplicar(self, a, b):
        resultado = a * b
        return resultado
        
    def dividir(self, a, b):
        if (a == 0 or b == 0):
            print("Não é possível dividir!")
        else:
            resultado = a / b
            return resultado

class CalculadoraCientifica(Calculadora):
    def __init__(self, marca, modelo, ano, funcoes_cientificas):
        super().__init__(marca, modelo, ano)

    def potencia(self, base, expoente):
        resultado = base ** expoente
        return resultado

    def raizQuadrada(self, numero):
        resultado = math.sqrt(numero)
        return resultado

# Crie uma classe CalculadoraCientifica que herda de Calculadora e adicione:

# Atributo: funcoes_cientificas (descrição str das funções científicas existentes)
# Método: potencia(base, expoente)
# Método: raiz_quadrada(numero)