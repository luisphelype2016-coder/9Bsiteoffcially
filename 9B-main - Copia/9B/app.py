from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "segredo"

admins = ["rafaela","hyllana","ph","yarley","otavio"] # você pode adicionar os admins aqui
usuarios = {

# você adiciona os alunos aqui

    "cecilia": "12",
    "arielly": "23",
    "enzo": "34",
    "fabio": "45",
    "hitallo": "56",
    "hyllana": "67",
    "isabella": "78",
    "lara": "89",
    "lavina": "901",
    "leda": "1011",
    "ph": "1121",
    "otavio": "1231",
    "luiza": "1341",
    "paula": "1451",
    "marina": "1561",
    "rafaela": "1671",
    "ryan": "1781",
    "thayla": "1891",
    "yarley": "6767",
    "zacarias": "2012",
    "leoncio": "2122",
    "neto": "2232",
    "rayka": "2342",
    "hanna": "2452",
    "eliz": "2562",
    "visgueira": "2672"

}

# ---------------- BANCO AUTO ----------------
def conectar():
    return sqlite3.connect("database.db")

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
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
    """)

    conn.commit()
    conn.close()

criar_banco()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["usuario"] = request.form["username"]
        return redirect("/home")
    return render_template("login.html")

# ---------------- HOME ----------------
@app.route("/home")
def home():
    return render_template("home.html")

# ---------------- TEMA ----------------
@app.route("/mudar_tema/<tema>")
def mudar_tema(tema):
    session["tema"] = tema
    return ""

# ---------------- ASSUNTOS ----------------
@app.route("/assuntos", methods=["GET","POST"])
def assuntos():

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        titulo = request.form.get("titulo")
        texto = request.form.get("texto")

        cursor.execute(
        "INSERT INTO assuntos (titulo,texto,autor) VALUES (?,?,?)",
        (titulo,texto,session["usuarios"])
        )

        conn.commit()

    lista = cursor.execute("SELECT * FROM assuntos").fetchall()

    conn.close()

    return render_template("assuntos.html", assuntos=lista)

# ---------------- ATIVIDADES ----------------
@app.route("/atividades", methods=["GET", "POST"])
def atividades():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        texto = request.form["texto"]
        img = request.files["imagem"]

        caminho = ""
        if img:
            caminho = "static/uploads/imagens/" + img.filename
            img.save(caminho)

        cursor.execute("INSERT INTO atividades VALUES (NULL,?,?,?)",
                       (texto, caminho, session["usuario"]))
        conn.commit()

    dados = cursor.execute("SELECT * FROM atividades").fetchall()
    conn.close()
    return render_template("atividades.html", atividades=dados)

# ---------------- GRUPOS ----------------
@app.route("/grupos", methods=["GET", "POST"])
def grupos():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        cursor.execute("INSERT INTO grupos VALUES (NULL,?,?)",
                       (nome, session["usuario"]))
        conn.commit()

    dados = cursor.execute("SELECT * FROM grupos").fetchall()
    conn.close()
    return render_template("grupos.html", grupos=dados)

# ---------------- CHAT GRUPO ----------------
@app.route("/grupo/<int:id>", methods=["GET", "POST"])
def chat_grupo(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        msg = request.form["mensagem"]
        data = datetime.now().strftime("%d/%m %H:%M")

        cursor.execute("INSERT INTO mensagens VALUES (NULL,?,?,?,?)",
                       (id, session["usuario"], msg, data))
        conn.commit()

    msgs = cursor.execute("SELECT * FROM mensagens WHERE grupo_id=?", (id,)).fetchall()
    conn.close()

    return render_template("chat_grupo.html", mensagens=msgs)

# ---------------- REDAÇÕES ----------------
@app.route("/redacoes", methods=["GET", "POST"])
def redacoes():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        texto = request.form["texto"]
        img = request.files["imagem"]

        caminho = ""
        if img:
            caminho = "static/uploads/redacoes/" + img.filename
            img.save(caminho)

        cursor.execute("INSERT INTO redacoes VALUES (NULL,?,?,?,NULL)",
                       (session["usuario"], texto, caminho))
        conn.commit()

    dados = cursor.execute("SELECT * FROM redacoes").fetchall()
    conn.close()
    return render_template("redacoes.html", redacoes=dados)

# ---------------- SLIDES ----------------
@app.route("/slides", methods=["GET", "POST"])
def slides():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        arq = request.files["arquivo"]

        caminho = "static/uploads/slides/" + arq.filename
        arq.save(caminho)

        cursor.execute("INSERT INTO slides VALUES (NULL,?,?)",
                       (session["usuario"], caminho))
        conn.commit()

    dados = cursor.execute("SELECT * FROM slides").fetchall()
    conn.close()
    return render_template("slides.html", slides=dados)

# ---------------- LOJAS ----------------
@app.route("/lojas", methods=["GET", "POST"])
def lojas():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        cat = request.form["categoria"]

        cursor.execute("INSERT INTO lojas VALUES (NULL,?,?,?)",
                       (nome, cat, session["usuario"]))
        conn.commit()

    dados = cursor.execute("SELECT * FROM lojas").fetchall()
    conn.close()
    return render_template("lojas.html", lojas=dados)

@app.route("/deletar_assunto/<int:id>")
def deletar_assunto(id):

    if "usuarios" not in session:
        return redirect("/")

    if session["usuarios"] not in admins:
        return "Você não tem permissão para excluir"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assuntos WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/assuntos")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)