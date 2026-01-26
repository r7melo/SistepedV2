from .db import get_db_connection

def listar_disciplinas_por_professor(id_professor):
    """Lista apenas as disciplinas vinculadas ao professor logado."""
    conn = get_db_connection()
    resultados = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Join entre Disciplina e ProfessorDisciplina para filtrar por professor
            query = """
                SELECT d.idDisciplina, d.nome 
                FROM Disciplina d
                INNER JOIN ProfessorDisciplina pd ON d.idDisciplina = pd.idDisciplina
                WHERE pd.idProfessor = %s
                ORDER BY d.nome ASC
            """
            cursor.execute(query, (id_professor,))
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar disciplinas: {e}")
        finally:
            cursor.close()
            conn.close()
    return resultados

def criar_disciplina_com_vinculo(nome, id_professor):
    """Cria a disciplina e vincula ao professor logado (ProfessorDisciplina)."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        
        # 1. Insere a disciplina
        cursor.execute("INSERT INTO Disciplina (nome) VALUES (%s)", (nome,))
        id_disciplina = cursor.lastrowid # Pega o ID gerado
        
        # 2. Cria o vínculo na tabela ProfessorDisciplina
        query_vinculo = "INSERT INTO ProfessorDisciplina (idProfessor, idDisciplina) VALUES (%s, %s)"
        cursor.execute(query_vinculo, (id_professor, id_disciplina))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar disciplina e vínculo: {e}")
        if conn: conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def deletar_disciplina_seguro(id_disciplina, id_professor):
    """Remove a disciplina apenas se ela pertencer ao professor logado."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        
        # Primeiro removemos o vínculo para evitar erro de FK
        cursor.execute("DELETE FROM ProfessorDisciplina WHERE idDisciplina = %s AND idProfessor = %s", 
                       (id_disciplina, id_professor))
        
        # Depois removemos a disciplina
        cursor.execute("DELETE FROM Disciplina WHERE idDisciplina = %s", (id_disciplina,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        if conn: conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()