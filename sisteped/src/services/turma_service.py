from .db import get_db_connection

def listar_turmas(id_professor, busca=''):
    """Lista apenas as turmas vinculadas ao professor logado"""
    conn = get_db_connection()
    resultados = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT t.idTurma, t.nome, t.anoLetivo 
                FROM Turma t
                INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
                WHERE pt.idProfessor = %s 
                AND t.nome LIKE %s
                ORDER BY t.nome ASC
            """
            cursor.execute(query, (id_professor, f'%{busca}%'))
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar turmas: {e}")
        finally:
            cursor.close()
            conn.close()
            
    return resultados

def criar_turma(nome, ano_letivo, id_professor, id_escola=1):
    """
    Insere uma nova turma e cria automaticamente o vínculo 
    na tabela ProfessorTurma.
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        # 1. Insere a Turma
        query_turma = "INSERT INTO Turma (nome, anoLetivo, idEscola) VALUES (%s, %s, %s)"
        cursor.execute(query_turma, (nome, ano_letivo, id_escola))
        
        # Recupera o ID da turma recém-criada
        id_turma_criada = cursor.lastrowid

        # 2. Cria o vínculo na tabela ProfessorTurma
        query_vinculo = "INSERT INTO ProfessorTurma (idProfessor, idTurma) VALUES (%s, %s)"
        cursor.execute(query_vinculo, (id_professor, id_turma_criada))
        
        conn.commit()  
        return True
        
    except Exception as e:
        print(f"Erro ao criar turma e vínculo: {e}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

def obter_turma_por_id(id_turma, id_professor):
    """Busca os dados de uma turma específica validando o dono."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.* FROM Turma t
            INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
            WHERE t.idTurma = %s AND pt.idProfessor = %s
        """
        cursor.execute(query, (id_turma, id_professor))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def atualizar_turma(id_turma, nome, ano_letivo):
    """Atualiza os dados da turma no banco."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "UPDATE Turma SET nome = %s, anoLetivo = %s WHERE idTurma = %s"
        cursor.execute(query, (nome, ano_letivo, id_turma))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def deletar_turma(id_turma, id_professor):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM ProfessorTurma WHERE idTurma = %s AND idProfessor = %s", (id_turma, id_professor))
        
        cursor.execute("DELETE FROM Turma WHERE idTurma = %s", (id_turma,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar turma: {e}")
        if conn: conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()