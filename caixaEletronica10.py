saldo = 1000.00
escolha = 0

def saque(x):

    return x

while (escolha != 4):
    escolha = int(input("1 - Sacar\n2 - Depositar\n3 - Extrato\n4 - Sair"))
    if (escolha == 1):
        print(f"Saldo atual: {saldo}")
        valorSaque = float(input("Informe o valor que valor você deseja sacar: "))
        if (valorSaque <= saldo):
            x = saque(valorSaque)
        