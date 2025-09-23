from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    if not all([DB_NAME, DB_USER, DB_PASSWORD]):
        raise ValueError(
            "Credenciais do banco de dados não configuradas. "
        )
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
        raise

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        print("Banco de dados PostgreSQL inicializado e tabela 'users' verificada/criada.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (nome, email, senha_hash) VALUES (%s, %s, %s)",
                       (nome, email, senha_hash))
        conn.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'error': 'Email já cadastrado. Por favor, use outro email.'}), 409
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados durante o cadastro: {e}")
        return jsonify({'error': f'Erro interno ao cadastrar usuário: {e}'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro inesperado durante o cadastro: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor.'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, nome, email FROM users ORDER BY id ASC")
        usuarios = cursor.fetchall()

        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return jsonify({'error': f'Erro ao buscar usuários: {e}'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/usuarios/<int:user_id>', methods=['PUT'])
def update_usuario(user_id):
    data = request.get_json()

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email:
        return jsonify({'error': 'Nome e Email são obrigatórios para atualização.'}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if senha:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            cursor.execute("UPDATE users SET nome = %s, email = %s, senha_hash = %s WHERE id = %s",
                           (nome, email, senha_hash, user_id))
        else:
            cursor.execute("UPDATE users SET nome = %s, email = %s WHERE id = %s",
                           (nome, email, user_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({'error': 'Usuário não encontrado.'}), 404

        conn.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'error': 'Email já cadastrado para outro usuário.'}), 409
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados durante a atualização: {e}")
        return jsonify({'error': f'Erro interno ao atualizar usuário: {e}'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro inesperado durante a atualização: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor.'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/usuarios/<int:user_id>', methods=['DELETE'])
def delete_usuario(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({'error': 'Usuário não encontrado.'}), 404

        conn.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro no banco de dados durante a exclusão: {e}")
        return jsonify({'error': f'Erro interno ao excluir usuário: {e}'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro inesperado durante a exclusão: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor.'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    if not all([DB_NAME, DB_USER, DB_PASSWORD]):
        print("ERRO: As variáveis do banco de dados não foram carregadas.")
        exit(1)

    init_db()
    app.run(debug=True)
