from classes import Jogador, Equipe

jogadores = []
equipes = [] 

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

opcao = 7
while (opcao != 0):
    print(texto)
    opcao = int(input("Escolha uma opção: "))

    if(opcao == 1):
        print("--- Cadastrar Jogador ---")
        nome = input("Digite o nome do jogador: ")
        turma = input("Digite a turma: ")
        nickname = input("Digite o nickname: ")

        jogador = Jogador(nome, turma, nickname)
        jogadores.append(jogador)

        print("Jogador cadastrado com sucesso!")

    elif(opcao == 2):
        print("--- Cadastrar Equipe ---")
        nome = input("Digite o nome da equipe: ")
        jogo = input("Digite o jogo que a equipe irá jogar: ")

        equipe = Equipe(nome, jogo)
        equipes.append(equipe)

        print("Equipe cadastrada com sucesso!")

    elif(opcao == 3):
        print("--- Adicionar Jogador a uma Equipe ---")
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
        print("Equipes cadastradas:")
        if len(equipes) == 0:
            print("Não existem equipes cadastradas.")
        else:
            for i in range(len(equipes)):
                print(f"\n[{i + 1}]", end=" ")
                equipes[i].exibir_info()

    elif(opcao == 5):
        print("--- Jogadores da Equipe ---")
        if len(equipes) == 0:
            print("Não existem equipes cadastradas.")
        else:
            print("Equipes cadastradas:")
            for i in range(len(equipes)):
                print(f"{i + 1}. {equipes[i].nome_equipe} ({equipes[i].jogo})")
            escolha_equipe = int(input("Escolha o número da equipe: ")) - 1
            print(f"Jogadores da equipe {equipes[escolha_equipe].nome_equipe}")
            equipes[escolha_equipe].listar_jogadores()
        
    elif(opcao == 6):
        print("--- Busca de Jogador ---")
        if len(jogadores) == 0:
            print("Nenhum jogador cadastrado no sistema.")
        nickname_escolhido = input("Informe o nickname que deseja buscar: ")
        encontrado = 0
        for jogador in jogadores:
            if jogador.nickname == nickname_escolhido: 
                jogador.exibir_dados()
                encontrado = 1
                break
        if encontrado == 0:
            print("Não existe um jogador com esse nickname cadastrado.")

    elif(opcao == 0):
        print("Encerrando o sistema.")

    else:
        print("Escolha uma opção válida!")