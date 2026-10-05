# Aula 4 — SQLite e início do CRUD: cadastrar e listar

**Data:** 05/11/2026  
**Programas/pacotes utilizados:** Python 3, Flask, SQLite (`sqlite3`, já incluído no Python), Visual Studio Code, navegador e Git.

## Objetivos

- compreender banco de dados, tabela, coluna e registro;
- conhecer chaves primárias;
- criar o banco `biblioteca.db`;
- criar a tabela `livros`;
- executar `INSERT` e `SELECT`;
- integrar Flask e SQLite;
- tornar permanentes os cadastros realizados pelo formulário.

---

## 1. Por que precisamos de um banco?

Na aula anterior, os livros estavam em uma lista Python. Ao encerrar o programa, os dados desapareciam.

Um banco de dados permite persistência.

```text
Formulário HTML
      ↓
Flask / Python
      ↓
SQLite
      ↓
biblioteca.db
```

---

## 2. Conceitos fundamentais

Imagine a tabela `livros`:

| id | titulo | autor | ano | categoria |
|---:|---|---|---:|---|
| 1 | O Hobbit | Tolkien | 1937 | Fantasia |
| 2 | 1984 | George Orwell | 1949 | Ficção |

- **tabela:** conjunto de dados relacionados;
- **coluna:** característica armazenada;
- **registro/linha:** um item cadastrado;
- **chave primária:** identificador único.

---

## 3. Criando uma função de conexão

Em `app.py`:

```python
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path("database/biblioteca.db")

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao
```

`sqlite3.Row` permite acessar colunas pelo nome:

```python
livro["titulo"]
```

---

## 4. Criando a tabela

Crie uma função executada no início da aplicação:

```python
def criar_tabela():
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)

    conexao = conectar()
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
    conexao.close()
```

Antes de `app.run(...)`:

```python
criar_tabela()
```

---

## 5. SQL: INSERT

Comando conceitual:

```sql
INSERT INTO livros (titulo, autor, ano, categoria)
VALUES ('O Hobbit', 'Tolkien', 1937, 'Fantasia');
```

No Python, **não monte SQL concatenando texto digitado pelo usuário**.

Use parâmetros:

```python
conexao.execute(
    """
    INSERT INTO livros (titulo, autor, ano, categoria, editora, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (titulo, autor, ano, categoria, editora, descricao)
)
```

Os `?` representam valores enviados separadamente.

---

## 6. Cadastrando pelo Flask

```python
@app.route("/livros/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        ano = request.form["ano"].strip()
        categoria = request.form["categoria"].strip()
        editora = request.form["editora"].strip()
        descricao = request.form["descricao"].strip()

        if titulo == "" or autor == "":
            return "Título e autor são obrigatórios", 400

        ano = int(ano) if ano else None

        conexao = conectar()
        conexao.execute(
            """
            INSERT INTO livros
            (titulo, autor, ano, categoria, editora, descricao)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (titulo, autor, ano, categoria, editora, descricao)
        )
        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_livros"))

    return render_template("cadastrar.html")
```

---

## 7. SQL: SELECT

Todos os livros:

```sql
SELECT * FROM livros;
```

Ordenados por título:

```sql
SELECT * FROM livros ORDER BY titulo;
```

No Flask:

```python
@app.route("/livros")
def listar_livros():
    conexao = conectar()
    livros = conexao.execute(
        "SELECT * FROM livros ORDER BY titulo"
    ).fetchall()
    conexao.close()

    return render_template("livros.html", livros=livros)
```

---

## 8. Exibindo todos os campos

```html
<table class="table table-striped">
    <thead>
        <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Autor</th>
            <th>Ano</th>
            <th>Categoria</th>
            <th>Editora</th>
        </tr>
    </thead>
    <tbody>
        {% for livro in livros %}
        <tr>
            <td>{{ livro.id }}</td>
            <td>{{ livro.titulo }}</td>
            <td>{{ livro.autor }}</td>
            <td>{{ livro.ano or "-" }}</td>
            <td>{{ livro.categoria or "-" }}</td>
            <td>{{ livro.editora or "-" }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

---

## 9. Primeiro CRUD de verdade

CRUD significa:

| Letra | Operação | SQL | No projeto |
|---|---|---|---|
| C | Create | INSERT | cadastrar |
| R | Read | SELECT | listar/consultar |
| U | Update | UPDATE | editar |
| D | Delete | DELETE | excluir |

Nesta aula implementamos **C** e **R**.

Na próxima, completaremos **U** e **D**.

---

## 10. Atividade da aula

O aluno deverá:

1. criar `biblioteca.db` automaticamente;
2. criar a tabela `livros`;
3. cadastrar pelo menos cinco livros pelo navegador;
4. fechar o servidor;
5. abrir novamente;
6. confirmar que os dados continuam disponíveis;
7. mostrar os registros em uma tabela HTML.

### Dados de teste sugeridos

Use livros de autores e anos diferentes. Isso será útil nas aulas de filtros e relatórios.

---

## 11. Erros comuns

### `no such table: livros`

A função de criação da tabela não foi chamada ou o programa está acessando outro arquivo `.db`.

### `database is locked`

Alguma conexão pode ter ficado aberta. Confirme que `close()` é chamado.

### Ano vazio gera erro

Não tente fazer `int("")`.

```python
ano = int(ano) if ano else None
```

---

## 12. Commit

```bat
git add .
git commit -m "Aula 4 - SQLite cadastro e listagem"
```

> O banco contendo dados pessoais ou muitos PDFs não deve necessariamente ser versionado. Para a disciplina, mantenha `database/*.db` e `uploads/` fora do Git se indicado pelo professor.
