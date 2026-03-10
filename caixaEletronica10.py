saldo = 1000.00
escolha = 0

def saque(saldo, valorSaque):
    if (valorSaque <= saldo):
        saldo = saldo - valorSaque
    elif (valorSaque > saldo):
        print("⚠️ O valor do saque desejado é maior que o saldo atual.")
    elif (saldo == 0):
        print("Saldo Zerado")
    return saldo

def deposito(saldo, valorDeposito):
    saldo = saldo + valorDeposito
    return saldo

while (escolha != 4):
    escolha = int(input("1 - Sacar\n2 - Depositar\n3 - Extrato\n4 - Sair"))
    if (escolha == 1):
        print(f"Saldo atual: {saldo}")
        valorSaque = input("Informe o valor que valor você deseja sacar: ")
        saldo = saque(saldo, valorSaque)
    elif (escolha == 2):
        valorDeposito = input("Informe o valor que você deseja depositar.")
        saldo = deposito(saldo, valorDeposito)