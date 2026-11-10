import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "biblioteca.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    conexao = conectar()
    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano INTEGER,
                categoria TEXT,
                editora TEXT,
                descricao TEXT,
                arquivo_pdf TEXT
            )
        """)
        conexao.commit()
    finally:
        conexao.close()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/livros")
def listar_livros():
    conexao = conectar()
    try:
        livros = conexao.execute(
            "SELECT * FROM livros ORDER BY titulo"
        ).fetchall()
    finally:
        conexao.close()
    return render_template("livros.html", livros=livros)


@app.route("/livros/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        ano = request.form.get("ano", "").strip()
        categoria = request.form.get("categoria", "").strip()
        editora = request.form.get("editora", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not titulo or not autor:
            return "Título e autor são obrigatórios", 400

        try:
            ano = int(ano) if ano else None
        except ValueError:
            return "O ano deve ser um número inteiro", 400
        if ano is not None and not -(2**63) <= ano < 2**63:
            return "Ano fora do intervalo de inteiros do SQLite", 400

        conexao = conectar()
        try:
            conexao.execute(
                """
                INSERT INTO livros
                (titulo, autor, ano, categoria, editora, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (titulo, autor, ano, categoria, editora, descricao),
            )
            conexao.commit()
        finally:
            conexao.close()
        return redirect(url_for("listar_livros"))

    return render_template("cadastrar.html")


criar_tabela()

if __name__ == "__main__":
    app.run()
