# InfraPlus - MVP

Este é um Produto Mínimo Viável (MVP), o projeto ainda está em andamento.

## ✨ Funcionalidades

* **Cadastro (Create):** Adicionar novos usuários.
* **Listagem (Read):** Visualizar usuários existentes em uma tabela.
* **Atualização (Update):** Editar dados de usuários.
* **Exclusão (Delete):** Remover usuários.

## 🚀 Tecnologias

* **Backend:** Python 3 (Flask)
* **Banco de Dados:** PostgreSQL
* **Frontend:** HTML, CSS, JavaScript

## ⚙️ Como Rodar (Setup Local)

Siga os passos para colocar o projeto em funcionamento na sua máquina:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/RealVitu1/infraplus_mvp.git](https://github.com/RealVitu1/infraplus_mvp.git)
    cd infraplus_mvp # Ou a pasta do seu projeto
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    # No Windows (PowerShell):
    .\venv\Scripts\activate
    # No Linux/macOS:
    # source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Se `requirements.txt` não existir, rode `pip install Flask psycopg2-binary python-dotenv` e depois `pip freeze > requirements.txt`)*

4.  **Configure o Banco de Dados (PostgreSQL):**
    * Certifique-se que o PostgreSQL está rodando.
    * Crie um banco de dados e um usuário para o projeto.
    * Crie um arquivo `.env` na raiz do projeto com suas credenciais:
        ```
        DB_HOST=localhost
        DB_NAME=Infraplus
        DB_USER=victor
        DB_PASSWORD=victor
        ```

5.  **Execute o Aplicativo:**
    ```bash
    python app.py
    ```
    Acesse `http://127.0.0.1:5000/` no seu navegador.

## 👨‍💻 Contato

* **Victor Hugo** - [https://github.com/RealVitu1](https://github.com/RealVitu1)

---
