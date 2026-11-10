from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
livros = [
    {"id": 1, "titulo": "O Hobbit", "autor": "Tolkien", "ano": 1937},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "ano": 1949},
    {"id": 3, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899},
]


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/livros")
def listar_livros():
    return render_template("livros.html", livros=livros)


@app.route("/livros/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        if not titulo or not autor:
            return "Título e autor são obrigatórios", 400

        livro = {
            "id": len(livros) + 1,
            "titulo": titulo,
            "autor": autor,
            "ano": request.form.get("ano", ""),
            "categoria": request.form.get("categoria", ""),
            "editora": request.form.get("editora", ""),
            "descricao": request.form.get("descricao", ""),
        }
        livros.append(livro)
        return redirect(url_for("listar_livros"))

    return render_template("cadastrar.html")


if __name__ == "__main__":
    app.run()
