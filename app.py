from flask import Flask, render_template, request, redirect, session, jsonify
from cliente import Cliente

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    return render_template("cabecalho-rodape.html")

@app.route("/cadastro")
def pg_cadasatrar_form():
    return render_template("cadastro-login.html")

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

app.run(debug=True)