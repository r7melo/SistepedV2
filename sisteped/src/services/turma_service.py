from .db import get_db_connection

def listar_turmas():
    conn = get_db_connection()
    resultados = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT idTurma, nome, anoLetivo FROM Turma ORDER BY nome ASC"
            cursor.execute(query)
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar turmas: {e}")
        finally:
            cursor.close()
            conn.close()
            
    return resultados

def criar_turma(nome, ano_letivo, id_escola=1):
    """
    Insere uma nova turma no banco.
    Obs: id_escola é obrigatório no banco, fixamos em 1 por enquanto.
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        query = "INSERT INTO Turma (nome, anoLetivo, idEscola) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, ano_letivo, id_escola))
        
        conn.commit()  
        return True
        
    except Exception as e:
        print(f"Erro ao criar turma: {e}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


