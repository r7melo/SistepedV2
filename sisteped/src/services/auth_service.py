# src/services/auth_service.py
import json
from pathlib import Path
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

DB_CONFIG = {
    "host": config.get("DB_HOST"),
    "user": config.get("DB_USER"),
    "password": config.get("DB_PASSWORD"),
    "database": config.get("DB_NAME"),
    "port": config.get("DB_PORT")
}

def get_db_connection():
    """Cria conexão com o banco"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None

def criar_usuario(nome, email, senha):
    """Cria um novo usuário com senha criptografada"""
    conn = get_db_connection()
    if not conn:
        return False, "Erro de conexão com o banco."

    try:
        cursor = conn.cursor()
        
        # 1. Verifica se email já existe
        cursor.execute("SELECT Id FROM Users WHERE Email = %s", (email,))
        if cursor.fetchone():
            return False, "E-mail já cadastrado."

        # 2. Insere na tabela Users
        query_user = "INSERT INTO Users (Name, Email) VALUES (%s, %s)"
        cursor.execute(query_user, (nome, email))
        user_id = cursor.lastrowid

        # 3. Insere na tabela UserCredentials com HASH
        senha_hash = generate_password_hash(senha) # Criptografa aqui
        query_cred = "INSERT INTO UserCredentials (UserId, PasswordHash, Role) VALUES (%s, %s, 'User')"
        cursor.execute(query_cred, (user_id, senha_hash))

        conn.commit()
        return True, "Usuário cadastrado com sucesso!"

    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar usuário: {e}")
        return False, "Erro interno ao cadastrar."
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def validar_usuario(email, senha_informada):
    """Valida usuário comparando o hash da senha"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        
        # AQUI MUDOU: Buscamos o Hash do banco, não comparamos direto no SQL
        query = """
            SELECT u.Id, u.Name, u.Email, uc.Role, uc.PasswordHash
            FROM Users u
            INNER JOIN UserCredentials uc ON u.Id = uc.UserId
            WHERE u.Email = %s
        """
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        # Se achou o usuário, verifica a senha
        if user and check_password_hash(user['PasswordHash'], senha_informada):
            return user
        
        return None # Usuário não achado ou senha errada

    except Exception as e:
        print(f"Erro na validação: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()