#pip install arcade
import arcade, random

ALTURA = 600
LARGURA = 1000
TITULO = "Tangled The Game"

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("rapunzel_direita.png", scale=0.23)
        self.textura_direita = arcade.load_texture("rapunzel_direita.png")
        self.textura_esquerda = arcade.load_texture("rapunzel_esquerda.png")
        
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if (self.change_x > 0):
            self.texture = self.textura_direita
        elif (self.change_x < 0):
            self.texture = self.textura_esquerda

        if (self.right > LARGURA):
            self.change_x = 0
            self.right = LARGURA
        if (self.left < 0):
            self.change_x = 0
            self.left = 0
        if (self.top > ALTURA):
            self.change_y = 0
            self.top = ALTURA
        if (self.bottom < 0):
            self.change_y = 0
            self.bottom = 0

class Moeda(arcade.Sprite):
    def __init__ (self):
        super().__init__("pascal.png", scale=0.2)

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("pascal_especial.png", scale=0.07)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1

class Inimigo(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("gothel.png", scale=0.15)
        self.jogador = jogador
        self.movimento = 1.5

    def update(self, delta_time):
        if self.center_x < self.jogador.center_x: self.center_x += self.movimento
        elif self.center_x > self.jogador.center_x: self.center_x -= self.movimento
        
        if self.center_y < self.jogador.center_y: self.center_y += self.movimento
        elif self.center_y > self.jogador.center_y: self.center_y -= self.movimento

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

        arcade.draw_text("Pressione [F] para Jogar", 750, 160, arcade.color.WHITE, 18, anchor_x="center", )
        arcade.draw_text("Pressione [ESC] para Sair", 750, 100, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("Torre_de_Rapunzel.png")

        self.jogo_finalizado = False
        self.movimento = 4
        self.pontuacao = 0
        self.tempo = 0.0
        
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 0
        self.jogador.center_y = 0
        self.sprite_jogador.append(self.jogador)

        for i in range (3):
            self.especial = MoedaEspecial()
            self.especial.center_x = random.randint(0, LARGURA - 50)
            self.especial.center_y = random.randint(50, ALTURA - 50)
            self.especial.change_x = self.movimento
            self.especial.change_y = self.movimento
            self.sprite_moedas.append(self.especial)

        for i in range(50):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, LARGURA - 50)
            self.moeda_simples.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(self.moeda_simples)

        self.inimigo = Inimigo(self.jogador)
        self.inimigo.center_x = 850
        self.inimigo.center_y = 200
        self.sprite_inimigos.append(self.inimigo)
    
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

        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigos.draw()
        arcade.draw_text(f"Pontos: {self.pontuacao}", 10, 570, arcade.color.AZURE_MIST, 14)
        arcade.draw_text(f"Tempo: {self.tempo:.2f}s", 10, 550, arcade.color.AZURE_MIST, 14)


    def on_update(self, delta_time):
        if self.jogo_finalizado:
            return

        self.tempo += delta_time
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigos.update(delta_time)

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            if(moeda == self.especial):
                self.pontuacao += 3
            else:
                self.pontuacao += 1

        inimigos_atingidos = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigos)
        for inimigo in inimigos_atingidos:
            self.pontuacao -= 1
            inimigo.remove_from_sprite_lists()

        if len(self.sprite_moedas) == 0:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo)
            self.window.show_view(tela_final)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.jogador.change_y = -self.movimento
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = self.movimento
        elif key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = self.movimento

        elif key == arcade.key.BACKSPACE:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo)
            self.window.show_view(tela_final)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT or key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = 0
        if key == arcade.key.S or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = 0

class TelaFinal(arcade.View):
    def __init__(self, pontos, tempo):
        super().__init__()
        self.fundo = arcade.load_texture("TelaFinal.png")
        self.pontos = pontos
        self.tempo = tempo

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

        arcade.draw_text(f"Pontuação: {self.pontos}  |  Tempo: {self.tempo:.1f}s", 750, 210, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [R] para Jogar Novamente", 750, 160, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [ESC] para Sair", 750, 100, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    tela_inicial = TelaInicial()
    janela.show_view(tela_inicial)
    arcade.run()

if __name__ == "__main__":
    main()