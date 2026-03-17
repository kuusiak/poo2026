# def verifica_par(x):
#     if (x % 2 == 0):
#         return True
#     return False

# resp = int(input("Digite um número: "))
# if (verifica_par(resp)):
#     print(f"O número {resp} é par!")
# else:
#     print(f"O número {resp} é ímpar!")

def cDesconto(precos, p):
    for i in range(0, len(precos)):
        desconto = precos[i] * (p / 100)
        valor = precos[i] - desconto
        precos[i] = valor
    return precos

resp = 0
indiceP = 0
produtos = [""] * 10
precos = []
while (resp != 4):
    resp = int(input("1- Cadastrar Produto\n2- Listar Produtos\n3- Aplicar Desconto\n4- Sair\n"))
    if(resp == 1):
        print("Cadastrar Produto")
        pNome = input("Nome: ")
        pPreco = float(input("Preço: R$"))
        produtos[indiceP] = pNome
        indiceP += 1
        precos.append(pPreco)
    elif(resp == 2):
        print("Listar Produtos")
        for i in range(0, len(precos)):
            print(produtos[i], "-", precos[i])
    elif(resp == 3):
        print("Aplicar Desconto")
        vDesc = int(input("Informe a porcentagem do desconto: "))
        preco_final = cDesconto(precos, vDesc)
        for i in range(len(precos)):
            print(produtos[i], "-", preco_final[i])
    elif(resp == 4):
        print("Você escolheu sair.")
    else:
        print("Informe uma opção válida!\n")