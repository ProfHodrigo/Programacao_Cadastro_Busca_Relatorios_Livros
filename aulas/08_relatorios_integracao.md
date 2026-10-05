# Aula 8 — Relatórios tabulares, integração, testes e preparação do projeto final

**Data:** 03/12/2026  
**Programas/pacotes utilizados:** Python 3, Flask, SQLite, Bootstrap via CDN, Visual Studio Code, navegador e Git.

## Objetivos

- compreender funções de agregação SQL;
- criar relatórios com `COUNT`, `MIN`, `MAX` e `GROUP BY`;
- exibir relatórios como quadros e tabelas HTML;
- integrar todas as funcionalidades do projeto;
- realizar testes manuais organizados;
- revisar estrutura e usabilidade;
- preparar o projeto para apresentação da Aula 9.

---

## 1. O que significa “relatório” nesta disciplina?

Relatório não significa gráfico.

Nesta disciplina, relatório é uma página que resume dados por meio de **números, quadros e tabelas**.

Exemplo:

| Indicador | Valor |
|---|---:|
| Total de livros | 42 |
| Total de autores | 18 |
| Ano mais antigo | 1899 |
| Ano mais recente | 2026 |

E:

| Autor | Quantidade |
|---|---:|
| Machado de Assis | 5 |
| Clarice Lispector | 3 |
| George Orwell | 2 |

---

## 2. `COUNT`

Quantidade de livros:

```sql
SELECT COUNT(*) AS total
FROM livros;
```

No Python:

```python
resumo = conexao.execute(
    "SELECT COUNT(*) AS total FROM livros"
).fetchone()

print(resumo["total"])
```

---

## 3. Quantidade de autores diferentes

```sql
SELECT COUNT(DISTINCT autor) AS total_autores
FROM livros;
```

`DISTINCT` faz cada autor ser contado uma vez.

---

## 4. Livro mais antigo e mais recente por ano

```sql
SELECT MIN(ano) AS ano_mais_antigo,
       MAX(ano) AS ano_mais_recente
FROM livros
WHERE ano IS NOT NULL;
```

---

## 5. `GROUP BY`

Quantidade por autor:

```sql
SELECT autor, COUNT(*) AS quantidade
FROM livros
GROUP BY autor
ORDER BY quantidade DESC, autor;
```

Quantidade por ano:

```sql
SELECT ano, COUNT(*) AS quantidade
FROM livros
WHERE ano IS NOT NULL
GROUP BY ano
ORDER BY ano DESC;
```

Quantidade por categoria:

```sql
SELECT categoria, COUNT(*) AS quantidade
FROM livros
WHERE categoria IS NOT NULL AND categoria <> ''
GROUP BY categoria
ORDER BY quantidade DESC, categoria;
```

---

## 6. Rota de relatórios

```python
@app.route("/relatorios")
def relatorios():
    conexao = conectar()

    resumo = conexao.execute("""
        SELECT
            COUNT(*) AS total_livros,
            COUNT(DISTINCT autor) AS total_autores,
            MIN(ano) AS ano_mais_antigo,
            MAX(ano) AS ano_mais_recente
        FROM livros
    """).fetchone()

    por_autor = conexao.execute("""
        SELECT autor, COUNT(*) AS quantidade
        FROM livros
        GROUP BY autor
        ORDER BY quantidade DESC, autor
    """).fetchall()

    por_ano = conexao.execute("""
        SELECT ano, COUNT(*) AS quantidade
        FROM livros
        WHERE ano IS NOT NULL
        GROUP BY ano
        ORDER BY ano DESC
    """).fetchall()

    por_categoria = conexao.execute("""
        SELECT categoria, COUNT(*) AS quantidade
        FROM livros
        WHERE categoria IS NOT NULL AND categoria <> ''
        GROUP BY categoria
        ORDER BY quantidade DESC, categoria
    """).fetchall()

    conexao.close()

    return render_template(
        "relatorios.html",
        resumo=resumo,
        por_autor=por_autor,
        por_ano=por_ano,
        por_categoria=por_categoria
    )
```

---

## 7. Quadro de resumo

```html
<div class="row g-3 mb-4">
    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h2>{{ resumo.total_livros }}</h2>
                <p>Total de livros</p>
            </div>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h2>{{ resumo.total_autores }}</h2>
                <p>Autores diferentes</p>
            </div>
        </div>
    </div>
</div>
```

Não há necessidade de gráficos. Os cards apenas destacam números.

---

## 8. Tabela por autor

```html
<h2>Livros por autor</h2>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Autor</th>
            <th>Quantidade</th>
        </tr>
    </thead>
    <tbody>
        {% for item in por_autor %}
        <tr>
            <td>{{ item.autor }}</td>
            <td>{{ item.quantidade }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

Repita a ideia para ano e categoria.

---

## 9. Integração da navegação

O menu principal deverá permitir acesso fácil a:

```text
Início | Livros | Novo livro | Relatórios
```

Cada registro da listagem deverá permitir:

```text
Detalhes | Editar | Excluir | Baixar PDF (quando disponível)
```

---

## 10. Estrutura final sugerida

```text
biblioteca_virtual/
├── app.py
├── requirements.txt
├── .gitignore
├── database/
│   └── biblioteca.db
├── uploads/
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── livros.html
    ├── cadastrar.html
    ├── editar.html
    ├── detalhes.html
    └── relatorios.html
```

Para a turma iniciante, é aceitável manter a maior parte da lógica em `app.py`. Separar rotas, serviços e repositórios em vários módulos seria uma evolução para outra disciplina.

---

## 11. Checklist funcional do projeto final

### Cadastro

- [ ] cadastrar título e autor;
- [ ] cadastrar ano, categoria, editora e descrição;
- [ ] impedir título ou autor vazios;
- [ ] salvar dados no SQLite.

### Consulta

- [ ] listar livros;
- [ ] visualizar detalhes;
- [ ] editar;
- [ ] excluir.

### Busca

- [ ] buscar título;
- [ ] buscar autor;
- [ ] filtrar por ano;
- [ ] filtrar por categoria;
- [ ] combinar filtros.

### PDF

- [ ] upload de PDF;
- [ ] cadastro sem PDF continua possível;
- [ ] download;
- [ ] impedir extensão diferente de PDF.

### Relatórios

- [ ] total de livros;
- [ ] total de autores diferentes;
- [ ] ano mais antigo e mais recente;
- [ ] quantidade por autor;
- [ ] quantidade por ano;
- [ ] quantidade por categoria.

---

## 12. Testes manuais

Crie uma tabela de testes para o grupo:

| Nº | Ação | Resultado esperado | Resultado obtido |
|---:|---|---|---|
| 1 | cadastrar livro válido | registro aparece na lista | |
| 2 | título vazio | cadastro recusado | |
| 3 | editar autor | valor atualizado | |
| 4 | excluir registro | desaparece da lista | |
| 5 | buscar parte do título | registros compatíveis | |
| 6 | filtrar por ano | somente ano escolhido | |
| 7 | enviar PDF | download disponível | |
| 8 | enviar arquivo não PDF | upload recusado | |
| 9 | abrir relatórios | totais coerentes | |

O objetivo não é criar testes automatizados nesta disciplina, mas ensinar o hábito de verificar sistematicamente o comportamento do software.

---

## 13. README do projeto final

Cada equipe deverá possuir um `README.md` com:

- nome do projeto;
- integrantes;
- objetivo;
- funcionalidades;
- tecnologias;
- instruções de instalação;
- instruções para executar;
- observações conhecidas.

Exemplo de execução:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py app.py
```

---

## 14. Git e versão para apresentação

Antes de apresentar:

```bat
git status
git add .
git commit -m "Projeto final - versao de apresentacao"
```

Se o projeto estiver no GitHub, confirme que o commit mais recente foi enviado.

Não faça mudanças grandes poucos minutos antes da apresentação.

---

## 15. Preparação para a Aula 9

A apresentação deve demonstrar o sistema funcionando. Uma sequência simples é:

1. abrir a página inicial;
2. listar os livros;
3. cadastrar um novo livro com PDF;
4. editar um registro;
5. fazer uma busca;
6. aplicar um filtro;
7. baixar um PDF;
8. abrir os relatórios;
9. explicar brevemente como Flask e SQLite participam do sistema.

A Aula 9 é reservada às apresentações. Não há novo conteúdo técnico planejado.

---

## 16. Commit final da disciplina prática

```bat
git add .
git commit -m "Aula 8 - relatorios e integracao final"
```
