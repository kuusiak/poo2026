class Campus:
    def __init__(self):
        self.endereco = ""
        self.nome = ""
    
    def __str__(self):
        return f"Campus: {self.nome}"
    
class Aluno:
    def __init__(self):
        self.nome = ""
        self.cpf = ""
        self.data_nasc = ""

    def __str__(self):
        return f"Aluno: {self.nome}"
    
    def apresentar(self):
        print (f"O(a) {self.nome} nasceu em {self.data_nasc}")
        if(self.cpf == ""):
            print("O(a) estudante não cadastrou o CPF.")
        else:
            print("CPF:", self.cpf[0,3], "...")
    
enzo = Aluno()
enzo.nome = "Enzo"
enzo.cpf = "123.456.789-00"
enzo.data_nasc = "10/06/2008"
print (f"O {enzo.nome} nasceu em {enzo.data_nasc}")

maria = Aluno()
maria.nome = "Maria"
maria.cpf = "123.456.789-10"
maria.data_nasc = "20/01/2009"
print (f"A {maria.nome} nasceu em {maria.data_nasc}")