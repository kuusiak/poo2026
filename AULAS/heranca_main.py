from heranca_classes import Animal, Gato, Cachorro
mello = Gato("Mello", "gato", 4, "Jeanne")
print(f"Meu gato é o {mello.nome}")
mello.respirar()
mello.ronronar()

pandora = Cachorro("Pandora", "cachorro", 4)
pandora.respirar()
pandora.abanarRabo()
pandora.rugir()
