from flask import Flask, render_template, request, redirect, session, jsonify
from conexao import Connection
from cliente import Cliente

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    mycursor.execute(f"SELECT nome, foto, preco FROM tb_produtos")

    resultado_total = mycursor.fetchall()

    mycursor.execute(f"SELECT nome, foto, preco FROM tb_produtos ORDER BY num_vendas")

    resultado_vendas = mycursor.fetchall()

    # lista_produtos = []

    # for x  in resultado:
    #     lista_produtos.append({"nome":x[0], "foto":x[1], "preco":x[2]})

    return render_template("Pagina-inicial.html", campo_titulo="GG TECH HUB", campo_produtos_total = resultado_total, campo_produtos_vendas = resultado_vendas)

@app.route("/cadastro-login")
def pg_cadastrar_form():
    return render_template("cadastro-login.html", campo_titulo="Cadastro ou Login")

@app.route("/cadastro", methods=["POST"])
def pg_cadastro():
    dados = request.get_json()
    cpf = dados["cpf"]
    telefone = dados["telefone"]
    email = dados["email"]
    nome = dados["nome"]
    senha = dados["senha"]

    cliente = Cliente()

    if cliente.cadastrar(cpf, telefone, email, nome, senha):
        session["usuario"] = {"nome":nome,"cpf":cpf}
        return jsonify({'mensagem':'Cadastro OK'}), 200
    else:
        return {'mensagem':'ERRO'}, 500

@app.route("/login", methods=["GET","POST"])
def pg_login():
    cliente = Cliente()
    if request.method == "GET":
        if session.get("usuario","erro") == "Autenticado":   
            return redirect("/")
        else:
            return redirect("cadastro-login.html")
    else:
        email = request.form["email-login"]
        senha = request.form["senha-login"]

        cliente.logar(email, senha)

        if cliente.logado:
            session["usuario"] = {"nome":cliente.nome, "cpf":cliente.cpf}
            return redirect("/")
        else:
            session.clear()
            return redirect("/login")

@app.route("/produto-individual")
def produto_individual():
    return render_template("produto-individual.html", campo_titulo="Produto Individual")

app.run(debug=True)