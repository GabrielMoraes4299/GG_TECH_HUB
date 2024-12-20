from flask import Flask, render_template, request, redirect, session, jsonify
from conexao import Connection
from cliente import Cliente

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    myBD = Connection.conectar()

    mycursor = myBD.cursor()


    mycursor.execute(f"SELECT id_produto, nome, foto, preco FROM tb_produtos ORDER BY hora DESC")

    resultado_total = mycursor.fetchall()

    mycursor.execute(f"SELECT id_produto, nome, foto, preco FROM tb_produtos ORDER BY num_vendas")

    resultado_vendas = mycursor.fetchall()
    
    if "usuario" in session:
        status_usuario = True
        nome_usuario = session["usuario"]["nome"]
        cpf_usuario = session["usuario"]["cpf"]
    else:
        status_usuario = False
        nome_usuario = None
        cpf_usuario = None

    return render_template("Pagina-inicial.html", campo_cliente = status_usuario, campo_nome_cliente = nome_usuario, campo_cpf_cliente = cpf_usuario,campo_titulo="GG TECH HUB", campo_produtos_total = resultado_total, campo_produtos_vendas = resultado_vendas)

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
            return render_template("cadastro-login.html")
    else:
        email = request.form["email-login"]
        senha = request.form["senha-login"]

        cliente.logar(email, senha)

        if cliente.logado:
            session["usuario"] = {"nome":cliente.nome, "cpf":cliente.cpf}

            return redirect('/')
        else:
            session.clear()
            return redirect("/login")

@app.route("/produto-individual/<codigo>")
def pg_produto(codigo):
    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    mycursor.execute(f"SELECT nome, foto, preco, descricao, id_produto FROM tb_produtos WHERE id_produto = {codigo};")

    dados = mycursor.fetchone()
    
    mycursor.execute(f"SELECT avaliacao FROM tb_comentarios WHERE id_produto = {codigo}")
    
    avaliacoes = mycursor.fetchall()
    
    qnt_avaliacoes = len(avaliacoes)
    
    soma_avaliacoes = 0
    for i in avaliacoes:
        soma_avaliacoes += i[0]
    
    if qnt_avaliacoes == 0:
        media_avaliacoes = 0
    else:
        media_avaliacoes = int(soma_avaliacoes / qnt_avaliacoes)
    myBD.close()
    
    if "usuario" in session:
        status_usuario = True
        nome_usuario = session["usuario"]["nome"]
        cpf_usuario = session["usuario"]["cpf"]
    else:
        status_usuario = False
        nome_usuario = None
        cpf_usuario = None

    return render_template("produto-individual.html", campo_cliente = status_usuario, campo_nome_cliente = nome_usuario, campo_cpf_cliente = cpf_usuario,campo_titulo="Produto Individual", campo_nome = dados[0], campo_foto = dados[1], campo_preco = dados[2], campo_descricao = dados[3], campo_codigo = dados[4], campo_avaliacao = media_avaliacoes)

@app.route("/enviar_comentario", methods=["POST"])
def enviar_mensagem():
    dados = request.get_json()
    conteudo_comentario = dados["conteudo_comentario"]
    avaliacao = dados["avaliacao"]
    id_produto = dados["id_produto"]
    cpf = session["usuario"]["cpf"]

    print(f"{conteudo_comentario}, {avaliacao}, {id_produto}, {cpf}")

    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    mycursor.execute(f"INSERT INTO tb_comentarios (id_produto, CPF_cliente, conteudo, avaliacao) VALUES ('{id_produto}', '{cpf}', '{conteudo_comentario}', '{avaliacao}');")

    myBD.commit()

    return jsonify({}), 200

@app.route('/mostrar_comentarios/<id_produto>')
def mostrar_comentarios(id_produto):
    cliente = Cliente()

    lista_comentarios = cliente.mostrar_comentarios(id_produto)

    return jsonify(lista_comentarios), 200

@app.route("/categorias/<id_categoria>")
def pg_categorias(id_categoria):
    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    mycursor.execute(f"SELECT nome, foto, preco, id_produto FROM tb_produtos p, tb_categorias c WHERE p.id_categoria = c.id_categoria AND p.id_categoria = {id_categoria}")

    resultado = mycursor.fetchall()
    
    if "usuario" in session:
        status_usuario = True
        nome_usuario = session["usuario"]["nome"]
        cpf_usuario = session["usuario"]["cpf"]
    else:
        status_usuario = False
        nome_usuario = None
        cpf_usuario = None


    return render_template("produtos.html", campo_cliente = status_usuario, campo_nome_cliente = nome_usuario, campo_cpf_cliente = cpf_usuario, campo_resultado = resultado)

@app.route("/carrinho")
def carrinho():
    if "usuario" in session:
        status_usuario = True
        nome_usuario = session["usuario"]["nome"]
        cpf_usuario = session["usuario"]["cpf"]
    else:
        status_usuario = False
        nome_usuario = None
        cpf_usuario = None
        
    return render_template("carrinho.html", campo_cliente = status_usuario, campo_nome_cliente = nome_usuario, campo_cpf_cliente = cpf_usuario, campo_titulo = "Carrinho de Compras")

@app.route("/mostrar_carrinho")
def mostrar_carrinho():
    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    cpf_usuario = session["usuario"]["cpf"]

    mycursor.execute(f"SELECT nome, preco, quantidade, c.id_produto FROM tb_carrinho c, tb_produtos p WHERE p.id_produto = c.id_produto AND CPF_cliente = {cpf_usuario};")

    itens_carrinho = mycursor.fetchall()

    print(itens_carrinho)

    return jsonify(itens_carrinho), 200

@app.route("/addcarrinho/<produto>/<quantidade>", methods=["GET", "POST"])
def addcarrinho(produto, quantidade):
    if request.method == "GET":
        cpf_cliente = session["usuario"]["cpf"]
        id_produto = produto
        qnt_produtos = quantidade
        
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        mycursor.execute(f"SELECT * FROM tb_carrinho WHERE id_produto = {id_produto} AND CPF_cliente = {cpf_cliente}")

        dados = mycursor.fetchall()

        if len(dados) == 0:
            mycursor.execute(f"INSERT INTO tb_carrinho(id_produto, CPF_cliente, quantidade) VALUES ({id_produto},'{cpf_cliente}',{qnt_produtos});")
        elif len(dados) > 0:
            mycursor.execute(f"UPDATE tb_carrinho SET quantidade = quantidade + {qnt_produtos} WHERE id_produto = {id_produto} AND CPF_cliente = {cpf_cliente};")
        myBD.commit()
        
        return redirect(f"/produto-individual/{id_produto}")
    else:
        cpf_cliente = session["usuario"]["cpf"]
        id_produto = produto
        qnt_produtos = quantidade
        
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        mycursor.execute(f"SELECT * FROM tb_carrinho WHERE id_produto = {id_produto} AND CPF_cliente = {cpf_cliente}")

        dados = mycursor.fetchall()

        if len(dados) == 0:
            mycursor.execute(f"INSERT INTO tb_carrinho(id_produto, CPF_cliente, quantidade) VALUES ({id_produto},'{cpf_cliente}',{qnt_produtos});")
        elif len(dados) > 0:
            mycursor.execute(f"UPDATE tb_carrinho SET quantidade = {qnt_produtos} WHERE id_produto = {id_produto} AND CPF_cliente = {cpf_cliente};")
        myBD.commit()
        
        return redirect(f"/produto-individual/{id_produto}")
    
@app.route("/excluir-produto/<produto>", methods=["POST"])
def excluir_produto(produto):
    cpf_cliente = session["usuario"]["cpf"]
    id_produto = produto

    myBD = Connection.conectar()

    mycursor = myBD.cursor()

    mycursor.execute(f"DELETE FROM tb_carrinho WHERE id_produto = {id_produto} AND CPF_cliente = {cpf_cliente}")

    myBD.commit()
    
    return redirect(f"/produto-individual/{id_produto}")
    
@app.route("/logoff")
def pagina_logoff():
    session.clear()
    return redirect("/")

@app.route("/sobre-nos")
def sobre_nos():
    return render_template("sobre-nos.html")

@app.route("/perguntas-frequentes")
def perguntas_frequentes():
    return render_template("perguntas-frequentes.html")

@app.route("/fale-conosco")
def fale_conosco():
    return render_template("fale-conosco.html")

app.run(debug=True)