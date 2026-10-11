from peewee import *
import arcade, random, datetime

ALTURA = 600
LARGURA = 800
TITULO = "Clair Obscur: Expedition Coins"
COLOR_TEXT = arcade.types.Color.from_hex_string("#fcdc8d")
COLOR_TEXT_RANKING = arcade.types.Color.from_hex_string("#b1ae7c")

ESCALA_JOGADOR = 0.5
MOVIMENTO_JOGADOR = 4
GRAVIDADE = 0.5
FORCA_PULO = 16

VALOR_MOEDA = 1
VALOR_MOEDA_ESPECIAL = 3
QTD_MOEDAS = 25
QTD_MOEDAS_ESPECIAIS = 1
PONTUACAO_MAXIMA = (QTD_MOEDAS * VALOR_MOEDA) + (QTD_MOEDAS_ESPECIAIS * VALOR_MOEDA_ESPECIAL)

ARQUIVO_SPRITESHEET_JOGADOR = "jogador-spritesheet.png"
LARGURA_FRAME_JOGADOR = 113
ALTURA_FRAME_JOGADOR = 140
COLUNAS_SPRITESHEET_JOGADOR = 11
TOTAL_FRAMES_JOGADOR = 11
TEMPO_POR_FRAME_JOGADOR = 0.1

SPRITESHEET_EFEITO = "efeito.png"
ESCALA_EFEITO = 1
LARGURA_FRAME_EFEITO = 110
ALTURA_FRAME_EFEITO = 130
COLUNAS_EFEITO = 6
TOTAL_FRAMES_EFEITO =6
TEMPO_POR_FRAME_EFEITO = 0.1

ALERTA_TIMER = 0.35
TEMPO_INVENCIVEL = 1.5
TEMPO_FLASH = 0.3
TEMPO_TREMOR = 0.35
INTENSIDADE_TREMOR = 8

banco = SqliteDatabase("ranking.db")
class BaseModel(Model):
    class Meta:
        database = banco

class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"

def inicializar_banco():
    banco.connect(reuse_if_open=True)
    banco.create_tables([Pontuacao])


class Player(arcade.Sprite):
    DIREITA = 1
    ESQUERDA = -1

    def __init__(self):
        sheet = arcade.load_spritesheet(ARQUIVO_SPRITESHEET_JOGADOR)
        quadros = sheet.get_texture_grid(
            size=(LARGURA_FRAME_JOGADOR, ALTURA_FRAME_JOGADOR),
            columns=COLUNAS_SPRITESHEET_JOGADOR,
            count=TOTAL_FRAMES_JOGADOR,
        )

        self.textura_idle_direita = quadros[0]
        self.textura_pulo_direita = quadros[1]
        self.texturas_andando_direita = quadros[2:10]
        self.textura_queda_direita = quadros[10]

        self.textura_idle_esquerda = self.textura_idle_direita.flip_left_right()
        self.textura_pulo_esquerda = self.textura_pulo_direita.flip_left_right()
        self.texturas_andando_esquerda = [textura.flip_left_right() for textura in self.texturas_andando_direita]
        self.textura_queda_esquerda = self.textura_queda_direita.flip_left_right()

        super().__init__(self.textura_idle_direita, scale = ESCALA_JOGADOR)

        self.virado_para = self.DIREITA
        self.frame_atual = 0
        self.tempo_animacao = 0.0 

    def update(self, delta_time):
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x = 0

        if self.left < 0:
            self.left = 0
            self.change_x = 0

        if self.change_x > 0:
            self.virado_para = self.DIREITA
        elif self.change_x < 0:
            self.virado_para = self.ESQUERDA

        if self.change_y > 0:
            if self.virado_para == self.DIREITA:
                self.texture = self.textura_pulo_direita
            else:
                self.texture = self.textura_pulo_esquerda
            return
        elif self.change_y < 0:
            if self.virado_para == self.DIREITA:
                self.texture = self.textura_queda_direita
            else:
                self.texture = self.textura_queda_esquerda
            return

        if self.change_x == 0:
            self.frame_atual = 0
            self.tempo_animacao = 0.0

            if self.virado_para == self.DIREITA:
                self.texture = self.textura_idle_direita
            else:
                self.texture = self.textura_idle_esquerda
            return

        self.tempo_animacao += delta_time

        if self.tempo_animacao >= TEMPO_POR_FRAME_JOGADOR:
            self.tempo_animacao -= TEMPO_POR_FRAME_JOGADOR
            self.frame_atual = (self.frame_atual + 1) % len(self.texturas_andando_direita)

        if self.virado_para == self.DIREITA:
            self.texture = self.texturas_andando_direita[self.frame_atual]
        else:
            self.texture = self.texturas_andando_esquerda[self.frame_atual]


class Moeda(arcade.Sprite):
    def __init__ (self):
        super().__init__("moeda.png", scale = 0.75)
        self.valor = VALOR_MOEDA

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale = 0.95)
        self.valor = VALOR_MOEDA_ESPECIAL

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1

class Inimigo(arcade.Sprite):
    def __init__(self):
            super().__init__("paintress.png", scale=0.75)
    
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("dualliste.png", scale=0.1)
        self.jogador = jogador
        self.movimento = 1.65

    def update(self, delta_time):
        if self.center_x < self.jogador.center_x: self.center_x += self.movimento
        elif self.center_x > self.jogador.center_x: self.center_x -= self.movimento
        
class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("plataforma.png", scale = 0.15)
        self.center_x = x
        self.center_y = y

class Efeito(arcade.Sprite):
    def __init__(self, x, y):
        sheet = arcade.load_spritesheet(SPRITESHEET_EFEITO)
        quadros = sheet.get_texture_grid(
            size=(LARGURA_FRAME_EFEITO, ALTURA_FRAME_EFEITO),
            columns=COLUNAS_EFEITO,
            count=TOTAL_FRAMES_EFEITO,
        )

        self.texturas_efeito = quadros

        super().__init__(self.texturas_efeito[0], scale = ESCALA_EFEITO)

        self.center_x = x
        self.center_y = y
        self.frame_atual = 0
        self.tempo_animacao = 0.0

    def update(self, delta_time):
        self.tempo_animacao += delta_time

        if self.tempo_animacao >= TEMPO_POR_FRAME_EFEITO:
            self.tempo_animacao -= TEMPO_POR_FRAME_EFEITO
            self.frame_atual += 1

            if self.frame_atual >= len(self.texturas_efeito):
                self.remove_from_sprite_lists()
                return

            self.texture = self.texturas_efeito[self.frame_atual]


class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaInicial.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        arcade.draw_text("[F] Jogar", LARGURA / 2, 155, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[T] Tutorial", LARGURA / 2, 125, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[R] Ranking", LARGURA / 2, 95, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[S] Saber Mais", LARGURA / 2, 65, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[ESC] Sair", LARGURA / 2, 35, COLOR_TEXT, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.T:
            tela_tutorial = TelaTutorial()
            self.window.show_view(tela_tutorial)
        elif key == arcade.key.R:
            tela_ranking = TelaRanking()
            self.window.show_view(tela_ranking)
        elif key == arcade.key.S:
            tela_sobre = TelaSobre()
            self.window.show_view(tela_sobre)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaJogo.png")

        self.jogo_finalizado = False
        self.dano = False
        self.alerta_timer = 0
        self.invencivel_timer = 0
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0
        self.camera = arcade.Camera2D()
        self.movimento = MOVIMENTO_JOGADOR

        self.qtd_moedas = QTD_MOEDAS
        self.qtd_moedas_especiais = QTD_MOEDAS_ESPECIAIS

        self.pontuacao_maxima = PONTUACAO_MAXIMA

        self.pontuacao = 0
        self.tempo = 0.0
        
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_inimigoEspecial = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_efeitos = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 32
        self.jogador.center_y = 64
        self.sprite_jogador.append(self.jogador)

        self.sprite_blocos = arcade.SpriteList()
        for x in range(100, LARGURA - 50, 200):
            chao = Bloco(x = x, y = 20)
            self.sprite_blocos.append(chao)

        bloco_pos = [(180, 140), (640, 180), (400, 260), (220, 380), (540, 440)]
        for x, y in bloco_pos:
            plataforma = Bloco(x, y)
            self.sprite_blocos.append(plataforma)

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite = self.jogador,
            walls = self.sprite_blocos,
            gravity_constant = GRAVIDADE
        )

        for i in range (self.qtd_moedas_especiais):
            self.especial = MoedaEspecial()
            self.posicionar_moedas(self.especial)
            self.especial.change_x = self.movimento - 1
            self.especial.change_y = self.movimento - 1
            self.sprite_moedas.append(self.especial)

        for i in range(self.qtd_moedas):
            self.moeda_simples = Moeda()
            self.posicionar_moedas(self.moeda_simples)
            self.sprite_moedas.append(self.moeda_simples)

        self.inimigoEspecial = InimigoEspecial(self.jogador)
        self.inimigoEspecial.center_x = 850
        self.inimigoEspecial.center_y = 90
        self.sprite_inimigoEspecial.append(self.inimigoEspecial)

        self.engine_fisica_inimigo = arcade.PhysicsEnginePlatformer(
            player_sprite = self.inimigoEspecial,
            walls = self.sprite_blocos,
            gravity_constant = GRAVIDADE
        )
        
        self.inimigo = Inimigo()
        self.inimigo.center_x = random.randint(0, LARGURA - 50)
        self.inimigo.center_y = random.randint(50, ALTURA - 50)
        self.inimigo.change_x = self.movimento - 0.7
        self.inimigo.change_y = self.movimento - 0.7
        self.sprite_inimigos.append(self.inimigo)


    def distancia_blocos(self, sprite, margem=15):
        for bloco in self.sprite_blocos:
            if (sprite.right + margem > bloco.left and
                sprite.left - margem < bloco.right and
                sprite.top + margem > bloco.bottom and
                sprite.bottom - margem < bloco.top):
                return False
        return True

    def posicionar_moedas(self, moeda):
        distancia_moeda = 50
        while True:
            colisao = False

            moeda.center_x = random.randint(50, LARGURA - 50)
            moeda.center_y = random.randint(50, ALTURA - 50)
            
            for outra_moeda in self.sprite_moedas:
                distancia = arcade.get_distance_between_sprites(moeda, outra_moeda)
                if distancia < distancia_moeda:
                    colisao = True
                    break
            if not colisao:
                if not self.distancia_blocos(moeda):
                    colisao = True
                    
            if not colisao:
                break

    def respawn (self, inimigo):
        distancia_min = 300
        while True:
            colisao = False
            inimigo.center_x = random.randint(50, LARGURA - 50)
            inimigo.center_y = 90
            for jogador in self.sprite_jogador:
                distancia = arcade.get_distance_between_sprites(inimigo, jogador)
                if distancia < distancia_min:
                    colisao = True
                    break

            if not colisao:
                break

    
    def on_draw(self):
        self.clear()

        self.camera.use()
        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA + 2 * INTENSIDADE_TREMOR,
                height=ALTURA + 2 * INTENSIDADE_TREMOR
            )
        )

        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigoEspecial.draw()
        self.sprite_inimigos.draw()
        self.sprite_blocos.draw()
        self.sprite_efeitos.draw()

        self.window.default_camera.use()

        if self.tempo_flash > 0:
            alpha = int(120 * self.tempo_flash / TEMPO_FLASH)
            arcade.draw_rect_filled(
                arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
                (255, 0, 0, alpha)
            )

        arcade.draw_text(f"Pontos: {self.pontuacao}", 10, 570, COLOR_TEXT, 14)
        arcade.draw_text(f"Tempo: {self.tempo:.2f}s", 10, 550, COLOR_TEXT, 14)

    def on_update(self, delta_time):
        if self.jogo_finalizado:
            return

        self.engine_fisica.update()
        self.tempo += delta_time
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigoEspecial.update(delta_time)
        self.sprite_inimigos.update(delta_time)
        self.sprite_efeitos.update(delta_time)

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            self.pontuacao += moeda.valor

        self.invencivel_timer = max(0.0, self.invencivel_timer - delta_time)
        self.tempo_flash = max(0.0, self.tempo_flash - delta_time)
        self.tempo_tremor = max(0.0, self.tempo_tremor - delta_time)

        if self.invencivel_timer == 0:
            especiais_colididos = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigoEspecial)
            if especiais_colididos:
                self.pontuacao -= 1
                self.alertaDano(especiais_colididos[0])
                self.respawn(self.inimigoEspecial)
            else:
                inimigos_colididos = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigos)
                if inimigos_colididos:
                    self.pontuacao -= 1
                    self.alertaDano(inimigos_colididos[0])

        if self.dano:
            self.alerta_timer -= delta_time
            if self.alerta_timer <= 0:
                self.dano = False

        if self.invencivel_timer > 0:
            if int(self.invencivel_timer * 10) % 2 == 0:
                self.jogador.alpha = 80
            else:
                self.jogador.alpha = 255
        else:
            self.jogador.alpha = 255

        if self.tempo_tremor > 0:
            forca = INTENSIDADE_TREMOR * self.tempo_tremor / TEMPO_TREMOR
            self.camera.position = (
                LARGURA / 2 + random.uniform(-forca, forca),
                ALTURA / 2 + random.uniform(-forca, forca),
            )
        else:
            self.camera.position = (LARGURA / 2, ALTURA / 2)

        if len(self.sprite_moedas) == 0:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima)
            self.window.show_view(tela_final)

    def alertaDano(self, inimigo):
        self.dano = True
        self.alerta_timer = ALERTA_TIMER
        self.invencivel_timer = TEMPO_INVENCIVEL
        self.tempo_flash = TEMPO_FLASH
        self.tempo_tremor = TEMPO_TREMOR

        x = (self.jogador.center_x + inimigo.center_x) / 2
        y = (self.jogador.center_y + inimigo.center_y) / 2
        self.sprite_efeitos.append(Efeito(x, y))
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = self.movimento
        if key == arcade.key.W or key == arcade.key.SPACE or key == arcade.key.UP:
            if self.engine_fisica.can_jump():
                self.jogador.change_y = FORCA_PULO
        if key == arcade.key.G:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima)
            self.window.show_view(tela_final)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT or key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = 0
        if key == arcade.key.W or key == arcade.key.SPACE or key == arcade.key.UP:
            self.jogador.change_y = 0

class TelaFinal(arcade.View):
    def __init__(self, pontos, tempo, pontuacao_maxima):
        super().__init__()
        self.fundo = arcade.load_texture("TelaFinal.png")
        self.pontos = pontos
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima

        self.nome_jogador = ""
        self.salvo = False
        self.mensagem = "Digite seu nome e pressione [ENTER] para salvar."

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )
        if self.pontos >= self.pontuacao_maxima:
            arcade.draw_text("VITÓRIA PERFEITA!", LARGURA / 2, 470, arcade.color.GOLD, 22, anchor_x="center")
        else:
            arcade.draw_text("PARABÉNS! JOGO CONCLUÍDO", LARGURA / 2, 470, COLOR_TEXT, 22, anchor_x="center")
        arcade.draw_text(f"Pontuação: {self.pontos}/{PONTUACAO_MAXIMA}  |  Tempo: {self.tempo:.1f}s", LARGURA / 2, 410, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[R] Ranking", LARGURA / 2, 115, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[ESPAÇO] Jogar Novamente", LARGURA / 2, 65, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("[ESC] Sair", LARGURA / 2, 35, COLOR_TEXT, 18, anchor_x="center")

        if not self.salvo:
            arcade.draw_text("NOME DO JOGADOR:", LARGURA / 2, 300, COLOR_TEXT, 18, anchor_x="center")
            nome_visivel = self.nome_jogador if self.nome_jogador else "_"
            arcade.draw_text(nome_visivel, LARGURA / 2, 255, COLOR_TEXT, 18, anchor_x="center")
            arcade.draw_text(self.mensagem, LARGURA / 2, 205, COLOR_TEXT, 18, anchor_x="center")
        else:
            arcade.draw_text("Pontuação salva no ranking!", LARGURA / 2, 285, arcade.color.GREEN_YELLOW, 18, anchor_x="center")

    def on_text(self, text):
        if self.salvo:
            return

        if text.isprintable() and len(self.nome_jogador) < 20:
            self.nome_jogador += text

    def on_key_press(self, key, modifiers):
        if not self.salvo:
            if key == arcade.key.ESCAPE:
                tela_inicial = TelaInicial()
                self.window.show_view(tela_inicial)
            if key == arcade.key.BACKSPACE:
                self.nome_jogador = self.nome_jogador[:-1]
            elif key == arcade.key.ENTER:
                nome = self.nome_jogador.strip()

                if len(nome) < 3:
                    self.mensagem = "Digite pelo menos 3 caracteres antes de salvar."
                    return

                Pontuacao.create(
                    nome_jogador=nome,
                    pontos=self.pontos,
                    tempo_partida=self.tempo,
                )

                self.salvo = True
                self.mensagem = "Registro salvo com sucesso."

            return

        if key == arcade.key.SPACE:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.R:
            tela_ranking = TelaRanking()
            self.window.show_view(tela_ranking)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaTutorial(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaInfo.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        arcade.draw_text("COMO JOGAR", LARGURA/2, 450, COLOR_TEXT, 30, anchor_x="center")

        arcade.draw_text("Use W A S D ou ⬅ ⮕ ⬆ ⬇ para se mover", LARGURA/2, 420, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text(f"A Moeda Especial vale (+{VALOR_MOEDA_ESPECIAL} Pontos)", LARGURA/2, 390, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text(f"As Moedas valem (+{VALOR_MOEDA} Ponto)", LARGURA/2, 360, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("Os Inimigos fazem você perder (-1 Ponto)", LARGURA/2, 330, COLOR_TEXT, 18, anchor_x="center")
        arcade.draw_text("O Inimigo Especial te persegue e faz você perder (-1 Ponto)", LARGURA/2, 300, COLOR_TEXT, 18, anchor_x="center")

        arcade.draw_text("OBJETIVOS", LARGURA/2, 220, COLOR_TEXT, 30, anchor_x="center")
        arcade.draw_text("Colete todas as moedas para concluir o jogo!", LARGURA/2, 190, COLOR_TEXT, 18, anchor_x="center")

        arcade.draw_text("Pressione [T] ou [ESC] para voltar ao início", LARGURA/2, 90, COLOR_TEXT, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.T or key == arcade.key.ESCAPE: 
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaInfo.png")
        self.sprite_maria = arcade.SpriteList()

        self.maria = arcade.Sprite("mariaa.png", scale = 0.15)
        self.maria.center_x = 75
        self.maria.center_y = 100
        self.sprite_maria.append(self.maria)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )
        self.sprite_maria.draw()

        arcade.draw_text("Feito por Maria Vitória Santos Kusiak", LARGURA/2, 550, COLOR_TEXT, 22.5, anchor_x="center")
        arcade.draw_text("Trabalho de Programação Orientada à Objetos", LARGURA/2, 450, COLOR_TEXT, 22.5, anchor_x="center")
        arcade.draw_text("Desenvolvido com Python Arcade", LARGURA/2, 420, COLOR_TEXT, 22.5, anchor_x="center")
        arcade.draw_text("Pressione [S] ou [ESC] para Voltar", LARGURA/2, 30, COLOR_TEXT, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.S:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

class TelaRanking(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaInfo.png")

        self.melhores = list(
            Pontuacao.select()
            .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
            .limit(10)
        )
        
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        arcade.draw_text("TOP 10 - RANKING", LARGURA / 2, 535, COLOR_TEXT, 35, anchor_x="center")

        arcade.draw_text("Pos.", 100, 485, COLOR_TEXT_RANKING, 15)
        arcade.draw_text("Jogador", 170, 485, COLOR_TEXT_RANKING, 15)
        arcade.draw_text("Pontos", 470, 485, COLOR_TEXT_RANKING, 15)
        arcade.draw_text("Tempo", 590, 485, COLOR_TEXT_RANKING, 15)

        if not self.melhores:
            arcade.draw_text("Ainda não há pontuações registradas.", LARGURA / 2, ALTURA / 2, COLOR_TEXT_RANKING, 18, anchor_x="center")
        else:
            for indice, registro in enumerate(self.melhores):
                y = 445 - indice * 34

                arcade.draw_text(
                    f"{indice + 1}º", 105, y, COLOR_TEXT_RANKING, 15,)
                arcade.draw_text(
                    registro.nome_jogador, 170, y, COLOR_TEXT_RANKING, 15,)
                arcade.draw_text(
                    str(registro.pontos), 485, y, COLOR_TEXT, 15,)
                arcade.draw_text(
                    f"{registro.tempo_partida:.1f}s", 590, y, COLOR_TEXT_RANKING, 15,)

        arcade.draw_text("[F] Jogar", LARGURA / 2, 55, COLOR_TEXT_RANKING, 15, anchor_x="center")
        arcade.draw_text("[R] ou [ESC] Menu", LARGURA / 2, 30, COLOR_TEXT_RANKING, 15, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.ESCAPE or key == arcade.key.R:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

def main():
    inicializar_banco()

    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    tela_inicial = TelaInicial()
    janela.show_view(tela_inicial)
    arcade.run()

if __name__ == "__main__":
    main()