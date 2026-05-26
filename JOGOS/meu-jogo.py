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
        pass

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)
        arcade.set_background_color(arcade.color.BUBBLE_GUM)
        self.personagem = Player()
        self.personagem.center_x = 400
        self.personagem.center_y = 300
    
    def on_draw(self):
        self.clear()
        arcade.draw_sprite(self.personagem)

    def on_update(self, delta_time):
        pass

def main():
    tela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()

#https://www.spriters-resource.com/dreamcast/marvelvscapcom2newageofheroes/asset/555083/