# Aula 6 — Busca e filtros

**Data:** 19/11/2026  
**Programas/pacotes utilizados:** Python 3, Flask, SQLite, Visual Studio Code, navegador e Git.

## Objetivos

- receber parâmetros pela URL;
- compreender query strings;
- utilizar `WHERE`, `LIKE`, `AND` e `ORDER BY`;
- construir SQL dinamicamente sem concatenar valores do usuário;
- pesquisar por título;
- filtrar por autor, ano e categoria;
- combinar filtros.

---

## 1. O que é uma busca?

Listar todos os livros é diferente de selecionar apenas os registros que atendem a certos critérios.

Exemplos:

```text
Título contém: Python
Autor: Machado de Assis
Ano: 2020
Categoria: Tecnologia
```

No navegador, uma busca pode aparecer assim:

```text
/livros?busca=python&ano=2020
```

A parte após `?` é chamada de **query string**.

---

## 2. Lendo parâmetros GET

```python
busca = request.args.get("busca", "").strip()
autor = request.args.get("autor", "").strip()
ano = request.args.get("ano", "").strip()
categoria = request.args.get("categoria", "").strip()
```

O segundo argumento de `get` é o valor padrão.

---

## 3. `LIKE`

SQL:

```sql
SELECT *
FROM livros
WHERE titulo LIKE '%Python%';
```

O `%` representa qualquer sequência de caracteres.

Com parâmetro Python:

```python
conexao.execute(
    "SELECT * FROM livros WHERE titulo LIKE ?",
    (f"%{busca}%",)
)
```

---

## 4. Busca por título ou autor

```sql
SELECT *
FROM livros
WHERE titulo LIKE ? OR autor LIKE ?;
```

```python
termo = f"%{busca}%"

livros = conexao.execute(
    """
    SELECT * FROM livros
    WHERE titulo LIKE ? OR autor LIKE ?
    ORDER BY titulo
    """,
    (termo, termo)
).fetchall()
```

---

## 5. Filtros combinados

Precisamos montar condições de acordo com o que o usuário preencheu.

```python
sql = "SELECT * FROM livros WHERE 1=1"
parametros = []

if busca:
    sql += " AND (titulo LIKE ? OR autor LIKE ?)"
    termo = f"%{busca}%"
    parametros.extend([termo, termo])

if autor:
    sql += " AND autor = ?"
    parametros.append(autor)

if ano:
    sql += " AND ano = ?"
    parametros.append(int(ano))

if categoria:
    sql += " AND categoria = ?"
    parametros.append(categoria)

sql += " ORDER BY titulo"

livros = conexao.execute(sql, parametros).fetchall()
```

### Por que `WHERE 1=1`?

A condição sempre é verdadeira. Ela simplifica a montagem didática das condições seguintes, pois todas podem começar com `AND`.

---

## 6. Por que não concatenar o texto do usuário?

Evite:

```python
sql = "SELECT * FROM livros WHERE titulo = '" + busca + "'"
```

Prefira:

```python
sql = "SELECT * FROM livros WHERE titulo = ?"
parametros = [busca]
```

Além de evitar problemas com aspas, parâmetros são uma proteção importante contra injeção de SQL.

---

## 7. Formulário GET de pesquisa

No topo de `livros.html`:

```html
<form method="get" class="row g-2 mb-4">
    <div class="col-md-4">
        <input class="form-control"
               name="busca"
               placeholder="Título ou autor"
               value="{{ request.args.get('busca', '') }}">
    </div>

    <div class="col-md-2">
        <input class="form-control"
               type="number"
               name="ano"
               placeholder="Ano"
               value="{{ request.args.get('ano', '') }}">
    </div>

    <div class="col-md-3">
        <input class="form-control"
               name="categoria"
               placeholder="Categoria"
               value="{{ request.args.get('categoria', '') }}">
    </div>

    <div class="col-md-3">
        <button class="btn btn-primary">Filtrar</button>
        <a class="btn btn-secondary" href="{{ url_for('listar_livros') }}">Limpar</a>
    </div>
</form>
```

Como o método é GET, os filtros aparecem na URL. Isso é adequado para consultas.

---

## 8. Filtro por opções existentes

Em vez de digitar a categoria, podemos obter as categorias existentes:

```python
categorias = conexao.execute(
    """
    SELECT DISTINCT categoria
    FROM livros
    WHERE categoria IS NOT NULL AND categoria <> ''
    ORDER BY categoria
    """
).fetchall()
```

HTML:

```html
<select name="categoria" class="form-select">
    <option value="">Todas as categorias</option>
    {% for item in categorias %}
        <option value="{{ item.categoria }}">
            {{ item.categoria }}
        </option>
    {% endfor %}
</select>
```

`DISTINCT` remove repetições.

---

## 9. Mensagem para zero resultados

```html
{% if livros %}
    <!-- tabela -->
{% else %}
    <div class="alert alert-info">
        Nenhum livro encontrado com os filtros informados.
    </div>
{% endif %}
```

---

## 10. Contando resultados da busca

No template:

```html
<p>{{ livros|length }} resultado(s) encontrado(s).</p>
```

Isso não substitui os relatórios gerais da Aula 8; apenas informa quantos registros a busca atual retornou.

---

## 11. Atividade da aula

A tela de livros deverá permitir:

- busca parcial por título;
- busca parcial por autor;
- filtro de ano;
- filtro de categoria;
- combinação entre filtros;
- limpar filtros;
- informar quando nenhum livro for encontrado.

### Cenário de teste

Cadastre pelo menos 10 registros com:

- três autores diferentes;
- três categorias diferentes;
- pelo menos cinco anos diferentes.

Depois teste combinações como:

```text
categoria = Tecnologia
ano = 2024
```

---

## 12. Commit

```bat
git add .
git commit -m "Aula 6 - busca e filtros"
```
