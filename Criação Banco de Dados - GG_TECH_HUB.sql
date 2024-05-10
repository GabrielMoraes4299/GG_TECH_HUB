CREATE DATABASE bd_ggtech;

USE bd_ggtech;

CREATE USER 'equipe'@'%' IDENTIFIED BY '123456789';
GRANT ALL PRIVILEGES ON bd_ggtech.* TO 'equipe'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE TABLE tb_clientes(
	CPF VARCHAR(11) PRIMARY KEY,
    telefone VARCHAR(9) NOT NULL,
    email VARCHAR(64) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE tb_categorias(
	id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(20) NOT NULL
);

CREATE TABLE tb_produtos(
	id_produto BIGINT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    foto VARCHAR(400) NOT NULL,
    id_categoria INT NOT NULL,
    preco VARCHAR(50) NOT NULL,
    CONSTRAINT fk_produtos_categorias FOREIGN KEY (id_categoria) REFERENCES tb_categorias(id_categoria)
);

CREATE TABLE tb_comentarios(
	id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_produto BIGINT NOT NULL,
    CPF_cliente VARCHAR(11) NOT NULL,
    conteudo VARCHAR(300) NOT NULL,
    avaliacao TINYINT NOT NULL,
    CONSTRAINT fk_comentarios_produtos FOREIGN KEY (id_produto) REFERENCES tb_produtos(id_produto),
    CONSTRAINT fk_comentarios_clientes FOREIGN KEY (CPF_cliente) REFERENCES tb_clientes(CPF)
);

CREATE TABLE tb_carrinho (
	id INT AUTO_INCREMENT PRIMARY KEY,
    id_produto BIGINT NOT NULL,
    CPF_cliente VARCHAR(11) NOT NULL,
    quantidade INT NOT NULL,
    CONSTRAINT fk_carrinho_produtos FOREIGN KEY (id_produto) REFERENCES tb_produtos(id_produto),
    CONSTRAINT fk_carrinho_clientes FOREIGN KEY (CPF_cliente) REFERENCES tb_clientes(CPF)
);
