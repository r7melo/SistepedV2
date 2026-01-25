from .db import get_db_connection

def listar_notas():
    """Busca todas as notas lançadas com o nome do aluno e turma."""
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
                av.conteudo, -- Usado para extrair a disciplina
                al.nomeCompleto AS nome_aluno,
                t.nome AS nome_turma
            FROM Avaliacao av
            INNER JOIN Aluno al ON av.idAluno = al.idAluno
            LEFT JOIN Turma t ON al.idTurma = t.idTurma
            ORDER BY av.data DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Erro ao listar notas gerais: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_turmas():
    """Retorna todas as turmas cadastradas para o select."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idTurma, nome FROM Turma ORDER BY nome ASC")
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Erro ao listar turmas: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_alunos_por_turma(id_turma):
    """Retorna alunos de uma turma específica."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT idAluno, nomeCompleto 
            FROM Aluno 
            WHERE idTurma = %s 
            ORDER BY nomeCompleto ASC
        """
        cursor.execute(query, (id_turma,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Erro ao listar alunos da turma {id_turma}: {e}")
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
    """
    Lista simplificada de alunos (ID, Nome e Turma) para a tela de lançamento de notas.
    """
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Query simplificada: Apenas dados essenciais para identificação
        query = """
            SELECT 
                al.idAluno,
                al.nomeCompleto,
                t.nome AS turma
            FROM Aluno al
            LEFT JOIN Turma t ON al.idTurma = t.idTurma
        """
        
        params = []
        if termo_busca:
            query += " WHERE al.nomeCompleto LIKE %s OR t.nome LIKE %s"
            termo = f"%{termo_busca}%"
            params = [termo, termo]
            
        query += " ORDER BY al.nomeCompleto ASC"

        cursor.execute(query, params)
        alunos = cursor.fetchall()
        return alunos

    except Exception as e:
        print(f"Erro ao listar alunos para notas: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()