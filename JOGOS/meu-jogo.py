#pip install arcade
import arcade
import random

ALTURA = 600
LARGURA = 800
TITULO = "Meu Jogo"

class Player(arcade.Sprite):
    def __init__(self):
        self.textura_direita = arcade.load_texture("alucard_direita.png")
        self.textura_esquerda = arcade.load_texture("alucard_esquerda.png")
        super().__init__("alucard_direita.png", scale=0.25)
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
        super().__init__("ghost.png", scale=0.7)
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if (self.right > LARGURA) or (self.left < 0):
            self.change_x *= -1

        if (self.top > ALTURA) or (self.bottom < 0):
            self.change_y *= -1

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)
        arcade.set_background_color(arcade.color.ARSENIC)
        #self.fundo = arcade.load_texture("cenario.png")
        self.movimento = 3
        self.pontuacao = 0

        self.jogador = Player()
        self.jogador.center_x = 0
        self.jogador.center_y = 0
        #self.jogador.change_x = self.movimento
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.moeda = Moeda()
        self.moeda.center_x = 600
        self.moeda.center_y = 300

        self.moeda.change_x = self.movimento
        self.moeda.change_y = self.movimento

        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moedas.append(self.moeda)

        for i in range(25):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, LARGURA - 50)
            self.moeda_simples.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(self.moeda_simples)

    
    def on_draw(self):
        self.clear()

        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570, arcade.color.AZURE_MIST, 14)

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            
            if(moeda.change_x != 0):
                self.pontuacao += 3
            else:
                self.pontuacao += 1
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.jogador.change_y = -self.movimento
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = self.movimento
        elif key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = self.movimento

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT or key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = 0
        if key == arcade.key.S or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = 0

def main():
    tela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()

#https://www.spriters-resource.com/dreamcast/marvelvscapcom2newageofheroes/asset/555083/