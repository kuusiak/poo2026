from heranca_calculadora import Calculadora, CalculadoraCientifica
calculadora = Calculadora("", "", "")
calculadora.marca = input("Informe a marca da calculadora: ")
calculadora.modelo = input("Informe o modelo da calculadora: ")
calculadora.ano = input("Informe o ano da calculadora: ")

a = int(input("Informe o primeiro número: "))
b = int(input("Informe o segundo número: "))
print(f"A soma dos números é {calculadora.somar(a, b)}")
print(f"A subtração dos números é {calculadora.subtrair(a, b)}")
print(f"A multiplicação dos números é {calculadora.multiplicar(a, b)}")
print(f"A divisão dos números é {calculadora.dividir(a, b)}")

calcCientifica = CalculadoraCientifica("", "", "", )