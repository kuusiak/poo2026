from classes import Jogador, Equipe

jogadores = []
equipes = [] 

opcao = 7
while (opcao != 0):
    texto = """========================================
CAMPEONATO INTERCLASSE DE E-SPORTS
========================================
1. Cadastrar jogador
2. Cadastrar equipe
3. Adicionar jogador a uma equipe
4. Listar todas as equipes
5. Listar jogadores de uma equipe
6. Buscar jogador por nickname
0. Sair
========================================"""
    print(texto)
    opcao = int(input("Escolha uma opção: "))

    if(opcao == 1):
        nome = input("Digite o nome do jogador: ")
        turma = input("Digite a turma: ")
        nickname = input("Digite o nickname: ")

        jogador = Jogador(nome, turma, nickname)
        jogadores.append(jogador)

        print("Jogador cadastrado com sucesso!")

    elif(opcao == 2):
        nome = input("Digite o nome da equipe: ")
        jogo = input("Digite o jogo que a equipe irá jogar: ")

        equipe = Equipe(nome, jogo)
        equipes.append(equipe)

        print("Equipe cadastrada com sucesso!")

    elif(opcao == 3):
        if len(jogadores) == 0:
            print("Nenhum jogador cadastrado.")

        elif len(equipes) == 0:
            print("Nenhuma equipe cadastrada.")

        else:
            print("Jogadores cadastrados:")
            for i in range(len(jogadores)):
                print(f"{i + 1}. ", end="")
            jogadores[i].exibir_dados()

            escolha_jogador = int(input("Escolha o número do jogador: ")) - 1

            print("Equipes cadastradas:")
            for i in range(len(equipes)):
                print(f"{i + 1}. {equipes[i].nome_equipe} ({equipes[i].jogo})")

            escolha_equipe = int(input("Escolha o número da equipe: ")) - 1

            jogador = jogadores[escolha_jogador]
            equipe = equipes[escolha_equipe]
            equipe.adicionar_jogadores(jogador)

            print("Jogador adicionado à equipe com sucesso!")
    elif(opcao == 4):
        w

    elif(opcao == 5):
        w

    elif(opcao == 6):
        w

    else:
        print("Escolha uma opção válida!")