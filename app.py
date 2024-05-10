from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    return render_template("cabecalho-rodape.html")

@app.route("/cadastro")
def pg_cadasatrar_form():
    return render_template("cadastro-login.html")

@app.route("/cadastrar", methods=["POST"])
def pg_cadastro():
    if session.get("usuario","erro") == "Autenticado":
        return render_template("cadastro-login.html")
    else:
        return render_template("cadastro-login.html")

app.run(debug=True)