# Aula 7 — Upload e download de PDFs

**Data:** 26/11/2026  
**Programas/pacotes utilizados:** Python 3, Flask, Werkzeug (instalado como dependência do Flask), SQLite, Visual Studio Code, navegador e Git.

## Objetivos

- compreender upload de arquivos;
- configurar formulário `multipart/form-data`;
- receber arquivos com Flask;
- aceitar somente PDF;
- gerar nomes de arquivo mais seguros;
- armazenar no banco o nome/caminho do PDF;
- realizar download;
- remover o arquivo associado quando necessário.

---

## 1. Banco de dados não precisa guardar o PDF inteiro

Para este projeto didático, os PDFs serão salvos na pasta:

```text
uploads/
```

O banco guardará apenas o nome do arquivo:

```text
arquivo_pdf = "7_o_hobbit.pdf"
```

Fluxo:

```text
Usuário seleciona PDF
        ↓
Flask recebe o arquivo
        ↓
Arquivo salvo em uploads/
        ↓
Nome salvo na tabela livros
```

---

## 2. Configuração

No início de `app.py`:

```python
from pathlib import Path

PASTA_UPLOADS = Path("uploads")
PASTA_UPLOADS.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
```

Neste exemplo, arquivos maiores que aproximadamente 20 MB serão recusados.

---

## 3. Formulário de arquivo

Um formulário comum não envia arquivos corretamente sem `enctype`.

```html
<form method="post" enctype="multipart/form-data">
```

Campo:

```html
<div class="mb-3">
    <label class="form-label">Arquivo PDF</label>
    <input class="form-control"
           type="file"
           name="arquivo_pdf"
           accept="application/pdf,.pdf">
</div>
```

`accept` ajuda a interface, mas a validação também precisa existir no servidor.

---

## 4. Recebendo o arquivo

```python
arquivo = request.files.get("arquivo_pdf")
```

Texto vem de:

```python
request.form
```

Arquivo vem de:

```python
request.files
```

---

## 5. Validando extensão

```python
def pdf_valido(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() == "pdf"
```

Uso:

```python
if arquivo and arquivo.filename:
    if not pdf_valido(arquivo.filename):
        return "Apenas arquivos PDF são permitidos", 400
```

Para uma aplicação profissional seriam necessárias verificações adicionais. Para esta disciplina, a validação de extensão e limite de tamanho é suficiente como introdução.

---

## 6. `secure_filename`

Importe:

```python
from werkzeug.utils import secure_filename
```

Em vez de salvar diretamente um nome recebido do navegador:

```python
nome_seguro = secure_filename(arquivo.filename)
```

Podemos incluir o ID do livro para reduzir conflitos:

```python
nome_final = f"{id}_{nome_seguro}"
arquivo.save(PASTA_UPLOADS / nome_final)
```

---

## 7. Estratégia: cadastrar primeiro, salvar PDF depois

Ao inserir um livro:

```python
cursor = conexao.execute(
    """
    INSERT INTO livros
    (titulo, autor, ano, categoria, editora, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (titulo, autor, ano, categoria, editora, descricao)
)

id_livro = cursor.lastrowid
```

Agora podemos salvar o PDF usando o ID:

```python
arquivo = request.files.get("arquivo_pdf")

if arquivo and arquivo.filename:
    if not pdf_valido(arquivo.filename):
        conexao.rollback()
        conexao.close()
        return "Apenas PDF", 400

    nome_seguro = secure_filename(arquivo.filename)
    nome_final = f"{id_livro}_{nome_seguro}"
    arquivo.save(PASTA_UPLOADS / nome_final)

    conexao.execute(
        "UPDATE livros SET arquivo_pdf = ? WHERE id = ?",
        (nome_final, id_livro)
    )

conexao.commit()
```

---

## 8. Download

Importe:

```python
from flask import send_from_directory
```

Rota:

```python
@app.route("/livros/<int:id>/pdf")
def baixar_pdf(id):
    conexao = conectar()
    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()
    conexao.close()

    if livro is None or not livro["arquivo_pdf"]:
        return "PDF não encontrado", 404

    return send_from_directory(
        PASTA_UPLOADS,
        livro["arquivo_pdf"],
        as_attachment=True
    )
```

Na página de detalhes:

```html
{% if livro.arquivo_pdf %}
<a class="btn btn-primary"
   href="{{ url_for('baixar_pdf', id=livro.id) }}">
    Baixar PDF
</a>
{% else %}
<span class="text-muted">Sem PDF</span>
{% endif %}
```

---

## 9. Atualizando o PDF de um livro

Na edição, permita um novo arquivo opcional.

Se houver um arquivo antigo, ele pode ser removido após o novo upload.

```python
arquivo_antigo = livro["arquivo_pdf"]
```

Antes de apagar, verifique a existência:

```python
caminho_antigo = PASTA_UPLOADS / arquivo_antigo

if arquivo_antigo and caminho_antigo.exists():
    caminho_antigo.unlink()
```

Tenha cuidado para só excluir arquivos associados a registros do sistema.

---

## 10. Exclusão do livro e do PDF

Ao excluir o registro, recupere antes o nome do PDF.

Sequência recomendada:

1. consultar o livro;
2. guardar o nome do arquivo;
3. excluir registro do banco;
4. confirmar a transação;
5. remover o arquivo se existir.

---

## 11. O que não faremos

Para manter o escopo apropriado a iniciantes, não implementaremos nesta disciplina:

- armazenamento em nuvem;
- antivírus no upload;
- autenticação de usuários;
- leitura do conteúdo interno do PDF;
- DRM;
- controle de direitos autorais.

> Para o trabalho acadêmico, use PDFs que possam ser legalmente armazenados e compartilhados, como documentos próprios, obras em domínio público ou arquivos fornecidos especificamente para teste.

---

## 12. Atividade da aula

Implemente:

- upload opcional ao cadastrar;
- validação de `.pdf`;
- limite de tamanho;
- armazenamento em `uploads/`;
- nome do arquivo no banco;
- botão de download;
- mensagem **Sem PDF** quando não houver arquivo.

### Testes

- PDF válido;
- arquivo `.txt` renomeado apenas para testar o bloqueio de extensão simples;
- cadastro sem PDF;
- download de PDF existente;
- acesso a livro sem arquivo.

---

## 13. Commit

```bat
git add .
git commit -m "Aula 7 - upload e download de PDFs"
```
