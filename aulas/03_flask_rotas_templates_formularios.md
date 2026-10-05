# Aula 3 — Flask: rotas, templates e formulários

**Data:** 29/10/2026  
**Programas/pacotes utilizados:** Python 3, Flask, Visual Studio Code, navegador e Git.

## Objetivos

- compreender cliente, servidor, requisição e resposta;
- criar rotas Flask;
- renderizar templates HTML;
- reutilizar um layout base com Jinja2;
- criar formulários HTML;
- compreender GET e POST;
- receber dados de formulário no Python.

---

## 1. Como uma aplicação Flask funciona?

Quando acessamos:

```text
http://127.0.0.1:5000/livros
```

o navegador envia uma requisição. Flask identifica qual função corresponde à rota `/livros`, executa essa função e devolve uma resposta.

```text
Navegador -> GET /livros -> Flask -> função Python
Navegador <- HTML         <- Flask <- resultado
```

---

## 2. Rotas

Em `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/livros")
def listar_livros():
    return "Página de livros"

if __name__ == "__main__":
    app.run(debug=True)
```

Cada `@app.route(...)` associa um endereço a uma função.

---

## 3. Templates

Crie:

```text
templates/
├── base.html
├── index.html
├── livros.html
└── cadastrar.html
```

### `base.html`

```html
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block titulo %}Biblioteca{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">Biblioteca Virtual</a>
    </div>
</nav>

<main class="container">
    {% block conteudo %}{% endblock %}
</main>
</body>
</html>
```

### `index.html`

```html
{% extends "base.html" %}

{% block titulo %}Início{% endblock %}

{% block conteudo %}
<h1>Biblioteca Virtual</h1>
<p>Sistema para cadastro, busca e relatórios de livros.</p>
<a class="btn btn-primary" href="/livros">Ver livros</a>
{% endblock %}
```

---

## 4. Enviando dados do Python ao HTML

Temporariamente, usaremos uma lista em memória:

```python
livros = [
    {"id": 1, "titulo": "O Hobbit", "autor": "Tolkien", "ano": 1937},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "ano": 1949}
]

@app.route("/livros")
def listar_livros():
    return render_template("livros.html", livros=livros)
```

`livros.html`:

```html
{% extends "base.html" %}

{% block conteudo %}
<h1>Livros</h1>

<table class="table table-striped">
    <thead>
        <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Ano</th>
        </tr>
    </thead>
    <tbody>
        {% for livro in livros %}
        <tr>
            <td>{{ livro.titulo }}</td>
            <td>{{ livro.autor }}</td>
            <td>{{ livro.ano }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

---

## 5. GET e POST

Nesta disciplina, pense assim:

- **GET:** pedir uma página ou consultar dados;
- **POST:** enviar dados para criar ou alterar algo.

Exemplo:

```text
GET  /livros/cadastrar -> abre o formulário
POST /livros/cadastrar -> envia o formulário
```

---

## 6. Formulário de cadastro

`cadastrar.html`:

```html
{% extends "base.html" %}

{% block conteudo %}
<h1>Novo livro</h1>

<form method="post">
    <div class="mb-3">
        <label class="form-label">Título</label>
        <input class="form-control" type="text" name="titulo" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Autor</label>
        <input class="form-control" type="text" name="autor" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Ano</label>
        <input class="form-control" type="number" name="ano">
    </div>

    <div class="mb-3">
        <label class="form-label">Categoria</label>
        <input class="form-control" type="text" name="categoria">
    </div>

    <button class="btn btn-success">Salvar</button>
</form>
{% endblock %}
```

---

## 7. Recebendo o formulário

```python
from flask import Flask, render_template, request, redirect

@app.route("/livros/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = request.form["ano"]
        categoria = request.form["categoria"]

        print(titulo, autor, ano, categoria)

        return redirect("/livros")

    return render_template("cadastrar.html")
```

Nesta aula os dados podem ser apenas impressos ou acrescentados à lista. Na próxima aula serão gravados permanentemente no SQLite.

---

## 8. `url_for`

Evite espalhar endereços escritos manualmente.

```python
from flask import url_for
```

No template:

```html
<a href="{{ url_for('listar_livros') }}">Livros</a>
```

O nome usado em `url_for` corresponde ao nome da função da rota.

---

## 9. Validação simples no servidor

```python
titulo = request.form["titulo"].strip()
autor = request.form["autor"].strip()

if titulo == "" or autor == "":
    return "Título e autor são obrigatórios", 400
```

O atributo HTML `required` ajuda o usuário, mas não substitui a validação no servidor.

---

## 10. Atividade guiada

Construa as páginas:

```text
/
/livros
/livros/cadastrar
```

A listagem deverá ter:

- título da página;
- botão **Novo livro**;
- tabela Bootstrap;
- pelo menos três registros temporários.

O formulário deverá ter:

- título;
- autor;
- ano;
- categoria;
- editora;
- descrição.

---

## 11. Desafio

Após receber um `POST`, adicione o livro à lista em memória e redirecione para `/livros`.

Observe a limitação: ao reiniciar o servidor, todos os dados desaparecem. Isso é exatamente o problema que resolveremos na Aula 4.

---

## 12. Commit

```bat
git add .
git commit -m "Aula 3 - rotas templates e formularios"
```

---

## Revisão

O aluno deverá saber responder:

- o que é uma rota;
- o que faz `render_template`;
- o que é Jinja2;
- a diferença prática entre GET e POST;
- para que serve `request.form`;
- por que a lista em memória não é suficiente para um sistema real.
