import mysql.connector

# Configurações do Banco (Do seu Docker)
DB_CONFIG = {
    'host': 'localhost',
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