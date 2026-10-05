# Aula 5 — CRUD completo: visualizar, editar e excluir

**Data:** 12/11/2026  
**Programas/pacotes utilizados:** Python 3, Flask, SQLite, Visual Studio Code, navegador e Git.

## Objetivos

- consultar um registro pelo `id`;
- construir uma página de detalhes;
- utilizar `UPDATE`;
- utilizar `DELETE`;
- preencher um formulário com valores existentes;
- tratar registro inexistente;
- completar as quatro operações do CRUD.

---

## 1. O papel do ID

Dois livros podem ter o mesmo título. Por isso, não devemos usar o título como identificador principal.

```text
/livros/7
```

Nesse exemplo, `7` é o `id`.

---

## 2. Rota com parâmetro

```python
@app.route("/livros/<int:id>")
def detalhar_livro(id):
    conexao = conectar()
    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()
    conexao.close()

    if livro is None:
        return "Livro não encontrado", 404

    return render_template("detalhes.html", livro=livro)
```

No Jinja:

```html
<a href="{{ url_for('detalhar_livro', id=livro.id) }}">
    Detalhes
</a>
```

---

## 3. Página de detalhes

`templates/detalhes.html`:

```html
{% extends "base.html" %}

{% block conteudo %}
<h1>{{ livro.titulo }}</h1>

<dl>
    <dt>Autor</dt>
    <dd>{{ livro.autor }}</dd>

    <dt>Ano</dt>
    <dd>{{ livro.ano or "Não informado" }}</dd>

    <dt>Categoria</dt>
    <dd>{{ livro.categoria or "Não informada" }}</dd>

    <dt>Editora</dt>
    <dd>{{ livro.editora or "Não informada" }}</dd>

    <dt>Descrição</dt>
    <dd>{{ livro.descricao or "Sem descrição" }}</dd>
</dl>

<a class="btn btn-warning"
   href="{{ url_for('editar_livro', id=livro.id) }}">Editar</a>
{% endblock %}
```

---

## 4. SQL UPDATE

Conceito:

```sql
UPDATE livros
SET titulo = 'Novo título'
WHERE id = 3;
```

A cláusula `WHERE` é essencial. Sem ela, todos os registros podem ser alterados.

---

## 5. Rota de edição

```python
@app.route("/livros/<int:id>/editar", methods=["GET", "POST"])
def editar_livro(id):
    conexao = conectar()
    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()

    if livro is None:
        conexao.close()
        return "Livro não encontrado", 404

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        ano_texto = request.form["ano"].strip()
        categoria = request.form["categoria"].strip()
        editora = request.form["editora"].strip()
        descricao = request.form["descricao"].strip()

        if titulo == "" or autor == "":
            conexao.close()
            return "Título e autor são obrigatórios", 400

        ano = int(ano_texto) if ano_texto else None

        conexao.execute(
            """
            UPDATE livros
            SET titulo = ?, autor = ?, ano = ?, categoria = ?,
                editora = ?, descricao = ?
            WHERE id = ?
            """,
            (titulo, autor, ano, categoria, editora, descricao, id)
        )
        conexao.commit()
        conexao.close()

        return redirect(url_for("detalhar_livro", id=id))

    conexao.close()
    return render_template("editar.html", livro=livro)
```

---

## 6. Formulário preenchido

Trecho de `editar.html`:

```html
<input class="form-control"
       type="text"
       name="titulo"
       value="{{ livro.titulo }}"
       required>
```

Ano:

```html
<input class="form-control"
       type="number"
       name="ano"
       value="{{ livro.ano or '' }}">
```

Textarea:

```html
<textarea class="form-control" name="descricao">{{ livro.descricao or '' }}</textarea>
```

---

## 7. SQL DELETE

```sql
DELETE FROM livros WHERE id = 3;
```

Novamente, `WHERE` é fundamental.

---

## 8. Exclusão por POST

Excluir altera dados, portanto não devemos usar apenas um link GET.

```python
@app.route("/livros/<int:id>/excluir", methods=["POST"])
def excluir_livro(id):
    conexao = conectar()
    conexao.execute(
        "DELETE FROM livros WHERE id = ?",
        (id,)
    )
    conexao.commit()
    conexao.close()

    return redirect(url_for("listar_livros"))
```

No HTML:

```html
<form method="post"
      action="{{ url_for('excluir_livro', id=livro.id) }}"
      onsubmit="return confirm('Deseja realmente excluir este livro?')">
    <button class="btn btn-danger">Excluir</button>
</form>
```

O `confirm` é apenas uma conveniência de interface. A operação real continua ocorrendo no servidor.

---

## 9. Validação de ano

Podemos melhorar a validação:

```python
ano = None

if ano_texto:
    try:
        ano = int(ano_texto)
    except ValueError:
        return "Ano inválido", 400
```

Podemos ainda verificar intervalo:

```python
if ano is not None and (ano < 0 or ano > 2100):
    return "Ano fora do intervalo permitido", 400
```

---

## 10. Atividade da aula

Implemente:

- botão **Detalhes** na tabela;
- página de detalhes;
- botão **Editar**;
- formulário de edição preenchido;
- atualização no banco;
- botão **Excluir**;
- confirmação visual antes da exclusão;
- tratamento de `id` inexistente.

### Teste obrigatório

1. cadastre um livro;
2. anote seu ID;
3. altere o título;
4. confirme a mudança na listagem;
5. exclua o livro;
6. tente abrir manualmente a URL antiga;
7. confirme a resposta de registro não encontrado.

---

## 11. Estado do projeto

Neste momento temos:

```text
[✓] Create
[✓] Read
[✓] Update
[✓] Delete
[ ] Busca e filtros
[ ] PDF
[ ] Relatórios
```

---

## 12. Commit

```bat
git add .
git commit -m "Aula 5 - CRUD completo"
```
