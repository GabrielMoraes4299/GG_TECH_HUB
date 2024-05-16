from flask import Flask, render_template, request, redirect, session, jsonify
from cliente import Cliente

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    return render_template("cabecalho-rodape.html")

@app.route("/cadastro-login")
def pg_cadastrar_form():
    return render_template("cadastro-login.html")

@app.route("/cadastro-login", methods=["POST"])
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

# @app.route("/cadastro-login", methods=["GET","POST"])
# def pg_login():
#     cliente = Cliente()
#     if request.method == "GET":
#         if session.get("usuario","erro") == "Autenticado":   
#             return redirect("/")
#         else:
#             return redirect("cadastro-login.html")
#     else:
#         email = request.form["email-login"]
#         senha = request.form["senha-login"]

#         cliente.logar(email, senha)

#         if cliente.logado:
#             session["usuario"] = {"nome":cliente.nome, "cpf":cliente.cpf}
#             return redirect("/")
#         else:
#             session.clear()
#             return redirect("/login")


app.run(debug=True)