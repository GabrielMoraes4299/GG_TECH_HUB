from conexao import Connection
from hashlib import sha256

class Cliente:
    def __init__(self) -> None:
        self.cpf = None
        self.telefone = None
        self.email = None
        self.nome = None
        self.senha = None
        self.logado = False

    def cadastrar(self, cpf, telefone, email, nome, senha):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.nome = nome
        self.senha = senha
        self.logado = True
        senha_criptografada = sha256(self.senha.encode()).hexdigest()

        mycursor.execute(f"INSERT INTO tb_clientes (CPF, telefone, email, nome, senha) VALUES ('{cpf}', '{telefone}','{email}', '{nome}','{senha_criptografada}');")

        myBD.commit()

        return True

    def logar(self, email, senha):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        self.email = email
        self.senha = senha
        senha_criptografada = sha256(self.senha.encode()).hexdigest()

        mycursor.execute(f"SELECT CPF, nome, email, senha FROM tb_clientes WHERE email = '{email}' AND BINARY senha = '{senha_criptografada}';")

        resultado = mycursor.fetchone()

        if resultado != None:
            self.logado = True
            self.cpf = resultado[0]
            self.nome = resultado[1]
            self.email = resultado[2]
            self.senha = resultado[3]
        else:
            self.logado = False
    
    def mostrar_comentarios(self, id_produto):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        mycursor.execute(f"SELECT nome, conteudo, avaliacao FROM tb_clientes ct, tb_comentarios cm WHERE ct.CPF = cm.CPF_cliente AND id_produto = {id_produto} ORDER BY id_comentario")

        resultado = mycursor.fetchall()

        lista_comentarios = []

        for x  in resultado:
            lista_comentarios.append({"nome":x[0], "conteudo":x[1], "avaliacao":x[2]})
        
        return (lista_comentarios)

    # def listar_contatos(self):
    #     myBD = Connection.conectar()

    #     mycursor = myBD.cursor()

    #     mycursor.execute(f"SELECT nome, tel FROM tb_usuario")

    #     resultado = mycursor.fetchall()

    #     for x in resultado:
    #         print("--------------------")
    #         print(f"| {x[0]} | {x[1]} |")
    #         print("--------------------")