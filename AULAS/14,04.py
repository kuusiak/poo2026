try:
    idade = int(input("idade: "))
    idade_nova = idade + 5
    print(f"Sua idade daqui 5 anos será {idade_nova}")
except Exception as erro:
    print("Idade inválida!")
    print(str(erro))