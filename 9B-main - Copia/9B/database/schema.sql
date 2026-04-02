CREATE TABLE IF NOT EXISTS usuarios (
id INTEGER PRIMARY KEY,
username TEXT,
senha TEXT,
tema TEXT
);

CREATE TABLE IF NOT EXISTS assuntos (
id INTEGER PRIMARY KEY,
texto TEXT,
imagem TEXT,
autor TEXT
);

CREATE TABLE IF NOT EXISTS atividades (
id INTEGER PRIMARY KEY,
texto TEXT,
imagem TEXT,
autor TEXT
);

CREATE TABLE IF NOT EXISTS grupos (
id INTEGER PRIMARY KEY,
nome TEXT,
criador TEXT
);

CREATE TABLE IF NOT EXISTS mensagens (
id INTEGER PRIMARY KEY,
grupo_id INTEGER,
autor TEXT,
mensagem TEXT,
datahora TEXT
);

CREATE TABLE IF NOT EXISTS redacoes (
id INTEGER PRIMARY KEY,
autor TEXT,
texto TEXT,
imagem TEXT,
nota TEXT
);

CREATE TABLE IF NOT EXISTS slides (
id INTEGER PRIMARY KEY,
autor TEXT,
arquivo TEXT
);

CREATE TABLE IF NOT EXISTS lojas (
id INTEGER PRIMARY KEY,
nome TEXT,
categoria TEXT,
criador TEXT
);

CREATE TABLE IF NOT EXISTS produtos (
id INTEGER PRIMARY KEY,
loja_id INTEGER,
nome TEXT,
descricao TEXT,
preco REAL
);

CREATE TABLE IF NOT EXISTS carrinho (
id INTEGER PRIMARY KEY,
usuario TEXT,
produto_id INTEGER,
quantidade INTEGER
);