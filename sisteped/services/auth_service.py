import mysql.connector
import os

# Configuração do banco de dados
DB_HOST = os.getenv('DB_HOST', 'host.docker.internal') 

DB_CONFIG = {
    'host': DB_HOST,
    'user': 'root',
    'password': 'DB!pass00',
    'database': 'sisteped',
    'port': 3306
}

def get_db_connection():
    """Cria conexão com o banco"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None

# ... o resto do seu código continua igual ...
def validar_usuario(email, senha):
    """Verifica se email e senha existem no banco"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        # Query com JOIN nas tabelas que criamos
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
        if conn.is_connected():
            cursor.close()
            conn.close()