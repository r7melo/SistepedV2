# src/services/auth_service.py
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection

def criar_usuario(nome, email, senha):
    """Cria um novo usuário com senha criptografada"""
    conn = get_db_connection()
    if not conn:
        return False, "Erro de conexão com o banco."

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT idProfessor FROM Professor WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "E-mail já cadastrado."

        senha_hash = generate_password_hash(senha) 
        
        query = "INSERT INTO Professor (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, email, senha_hash))

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
        
        query = "SELECT idProfessor, nome, email, senha FROM Professor WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
  
            if check_password_hash(user['senha'], senha_informada):
                return user
            
        return None

    except Exception as e:
        print(f"Erro na validação: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()