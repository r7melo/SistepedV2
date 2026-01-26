from .db import get_db_connection

def listar_notas(id_professor):
    """Busca as notas apenas dos alunos pertencentes às turmas do professor logado."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                av.idAvaliacao,
                av.nota,
                av.data,
                av.conteudo,
                al.nomeCompleto AS nome_aluno,
                t.nome AS nome_turma
            FROM Avaliacao av
            INNER JOIN Aluno al ON av.idAluno = al.idAluno
            INNER JOIN Turma t ON al.idTurma = t.idTurma
            INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
            WHERE pt.idProfessor = %s
            ORDER BY av.data DESC
        """
        cursor.execute(query, (id_professor,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar notas: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_turmas(id_professor):
    """Retorna apenas as turmas vinculadas ao professor logado."""
    conn = get_db_connection()
    if not conn:
        return []
    
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
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar turmas: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_alunos_por_turma(id_turma, id_professor):
    """Retorna alunos de uma turma específica, validando se o professor tem acesso a ela."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT al.idAluno, al.nomeCompleto 
            FROM Aluno al
            INNER JOIN ProfessorTurma pt ON al.idTurma = pt.idTurma
            WHERE al.idTurma = %s AND pt.idProfessor = %s
            ORDER BY al.nomeCompleto ASC
        """
        cursor.execute(query, (id_turma, id_professor))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar alunos da turma: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_alunos_notas(id_professor, termo_busca=None):
    """Lista alunos e suas turmas filtrando apenas pelo que o professor gerencia."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                al.idAluno,
                al.nomeCompleto,
                t.nome AS turma
            FROM Aluno al
            INNER JOIN Turma t ON al.idTurma = t.idTurma
            INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
            WHERE pt.idProfessor = %s
        """
        params = [id_professor]
        
        if termo_busca:
            query += " AND (al.nomeCompleto LIKE %s OR t.nome LIKE %s)"
            termo = f"%{termo_busca}%"
            params.extend([termo, termo])
            
        query += " ORDER BY al.nomeCompleto ASC"

        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar alunos para notas: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def salvar_avaliacao(titulo, disciplina, data, id_aluno, nota):
    """Salva uma única avaliação no banco."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        tipo = "Avaliação"
        conteudo_completo = f"{titulo} ({disciplina})"

        query = """
            INSERT INTO Avaliacao (conteudo, nota, data, tipo, idAluno)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (conteudo_completo, nota, data, tipo, id_aluno))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar avaliação para aluno {id_aluno}: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def atualizar_nota_individual(id_av, nota):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        query = "UPDATE Avaliacao SET nota = %s WHERE idAvaliacao = %s"
        cursor.execute(query, (nota, id_av))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro no banco: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def remover_nota_individual(id_av):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM Avaliacao WHERE idAvaliacao = %s"
        cursor.execute(query, (id_av,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao remover: {e}")
        return False
    finally:
        cursor.close()
        conn.close()