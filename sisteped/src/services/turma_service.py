from .db import get_db_connection

def listar_turmas(id_professor):
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
                ORDER BY t.nome ASC
            """
            cursor.execute(query, (id_professor,))
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