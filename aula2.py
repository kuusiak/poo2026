"""num = int (input("Digite um número qualquer: "))
if (num > 100):
    print (num/2)"""

"""num = int (input("Digite um número qualquer: "))
if (num % 2 == 0):
    print ("Seu número é par!")
else:
    print ("Seu número é ímpar!")"""

num = int (input("Digite um número qualquer: "))
sinal = input(("Digite também um operador matemático: "))
num2 = int(input("Digite um segundo número qualquer: "))
resultado = 0

if (sinal == "+"):
    resultado = num + num2
    print(f"O resultado da sua conta é: {resultado}")
elif (sinal == "-"):
    resultado = num - num2
    print(f"O resultado da sua conta é: {resultado}")
elif (sinal == "/"):
    resultado = num / num2
    print(f"O resultado da sua conta é: {resultado}")
elif (sinal == "*"):
    resultado = num * num2
    print(f"O resultado da sua conta é: {resultado}")