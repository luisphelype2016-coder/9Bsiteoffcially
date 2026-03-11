from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

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


def conectar():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        user = request.form.get("username")
        senha = request.form.get("password")

        if user in usuarios and usuarios[user] == senha:

            session["user"] = user
            return redirect("/home")

    return render_template("login.html")


@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    return render_template("home.html")


@app.route("/assuntos", methods=["GET","POST"])
def assuntos():

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        titulo = request.form.get("titulo")
        texto = request.form.get("texto")

        cursor.execute(
        "INSERT INTO assuntos (titulo,texto,autor) VALUES (?,?,?)",
        (titulo,texto,session["user"])
        )

        conn.commit()

    lista = cursor.execute("SELECT * FROM assuntos").fetchall()

    conn.close()

    return render_template("assuntos.html", assuntos=lista)


@app.route("/atividades", methods=["GET","POST"])
def atividades():

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        titulo = request.form.get("titulo")
        texto = request.form.get("texto")

        cursor.execute(
        "INSERT INTO atividades (titulo,texto,autor) VALUES (?,?,?)",
        (titulo,texto,session["user"])
        )

        conn.commit()

    lista = cursor.execute("SELECT * FROM atividades").fetchall()

    conn.close()

    return render_template("atividades.html", atividades=lista)


@app.route("/grupos", methods=["GET","POST"])
def grupos():

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        nome = request.form.get("nome_grupo")
        participantes = request.form.get("participantes")

        cursor.execute(
        "INSERT INTO grupos (nome,participantes,criador) VALUES (?,?,?)",
        (nome,participantes,session["user"])
        )

        conn.commit()

    lista = cursor.execute("SELECT * FROM grupos").fetchall()

    conn.close()

    return render_template("grupos.html", grupos=lista)


@app.route("/grupo/<int:id>", methods=["GET","POST"])
def chat_grupo(id):

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        mensagem = request.form.get("mensagem")

        from datetime import datetime
        datahora = datetime.now().strftime("%d/%m/%Y %H:%M")

        cursor.execute(
        "INSERT INTO mensagens (grupo_id,autor,mensagem,datahora) VALUES (?,?,?,?)",
        (id,session["user"],mensagem,datahora)
        )

        conn.commit()

    grupo = cursor.execute(
    "SELECT * FROM grupos WHERE id=?",(id,)
    ).fetchone()

    mensagens = cursor.execute(
    "SELECT * FROM mensagens WHERE grupo_id=?",(id,)
    ).fetchall()

    conn.close()

    return render_template(
    "grupo_chat.html",
    grupo=grupo,
    mensagens=mensagens
    )


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/deletar_assunto/<int:id>")
def deletar_assunto(id):

    if "user" not in session:
        return redirect("/")

    if session["user"] not in admins:
        return "Você não tem permissão para excluir"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assuntos WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/assuntos")

@app.route("/deletar_atividade/<int:id>")
def deletar_atividade(id):

    if "user" not in session:
        return redirect("/")

    if session["user"] not in admins:
        return "Você não tem permissão para excluir"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM atividades WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/atividades")

@app.route("/deletar_grupo/<int:id>")
def deletar_grupo(id):

    if "user" not in session:
        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    grupo = cursor.execute(
    "SELECT * FROM grupos WHERE id=?", (id,)
    ).fetchone()

    if grupo["criador"] != session["user"]:
        return "Só o criador pode excluir este grupo"

    cursor.execute("DELETE FROM grupos WHERE id=?", (id,))
    cursor.execute("DELETE FROM mensagens WHERE grupo_id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/grupos")

if __name__ == "__main__":

    app.run(debug=True)