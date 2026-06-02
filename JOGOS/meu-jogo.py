#pip install arcade
import arcade

ALTURA = 600
LARGURA = 800
TITULO = "Meu Jogo"

class Player(arcade.Sprite):
    def __init__(self):
        self.textura_direita = arcade.load_texture("player_direita.png")
        self.textura_esquerda = arcade.load_texture("player_esquerda.png")
        super().__init__("player_direita.png", scale=0.5)
    def uptade(self, delta_time):
        self.center_x += self.center_x
        self.center_y += self.center_y
        if (self.change_x > 0):
            self.texture = self.textura_direita
        elif (self.change_x < 0):
            self.texture = self.textura_esquerda

class Moeda(arcade.Sprite):
    def __init__ (self):
        super().__init__("ghost.png", scale=0.7)
    def uptade(self, delta_time):
        self.center_x += self.center_x
        self.center_y += self.center_y

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)
        arcade.set_background_color(arcade.color.BUBBLE_GUM)
        self.movimento = 3
        self.jogador = Player()
        self.jogador.center_x = 400
        self.jogador.center_y = 300
        self.jogador.change_x = self.movimento
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)
        self.moeda = Moeda()
        self.moeda.center_x = 600
        self.moeda.center_y = 300
        self.moeda.change_x = self.movimento
        self.moeda.change_y = self.movimento
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moedas.append(self.moeda)
    
    def on_draw(self):
        self.clear()
        self.sprite_jogador.draw()
        self.sprite_moedas.draw()

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)

def main():
    tela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()

#https://www.spriters-resource.com/dreamcast/marvelvscapcom2newageofheroes/asset/555083/