class Jogador:

    def __init__(self, nome_jogador, turma, nickname):
        self.nome_jogador = nome_jogador
        self.turma = turma
        self.nickname = nickname

    def exibir_dados(self):
        print(f"{self.nome_jogador} ({self.nickname}) - {self.turma}")

class Equipe:

    def __init__(self, nome_equipe, jogo):
        self.nome_equipe = nome_equipe
        self.jogo = jogo
        self.jogadores = []

    def adicionar_jogadores(self, jogador):
        self.jogadores.append(jogador)

    def listar_jogadores(self):
        if len(self.jogadores) == 0:
            print("Não há nenhum jogador.")
        else:
            for jogador in self.jogadores:
                jogador.exibir_dados()

    def exibir_info(self):
        print(f"Equipe: {self.nome_equipe} | Jogo: {self.jogo}")
        print(f"Quantidade de jogadores: {len(self.jogadores)}")