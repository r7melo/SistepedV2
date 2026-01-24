# src/services/auth_service.py
import json
from pathlib import Path
import mysql.connector

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

DB_CONFIG = {
    "host": config.get("DB_HOST", "localhost"),
    "user": config.get("DB_USER", "root"),
    "password": config.get("DB_PASSWORD", "DB!pass00"),
    "database": config.get("DB_NAME", "sisteped"),
    "port": config.get("DB_PORT", 3306)
}

def get_db_connection():
    """Cria conexão com o banco"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None

def validar_usuario(email, senha):
    """Verifica se email e senha existem no banco"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT u.Id, u.Name, u.Email, uc.Role 
            FROM Users u
            INNER JOIN UserCredentials uc ON u.Id = uc.UserId
            WHERE u.Email = %s AND uc.PasswordHash = %s
        """
        cursor.execute(query, (email, senha))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Erro na validação: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
