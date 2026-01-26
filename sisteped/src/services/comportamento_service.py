from .db import get_db_connection

def listar_comportamentos_professor(id_professor):
    """Lista os registros de comportamento vinculados ao professor logado."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.idComportamento, c.tag, c.observacao, a.nomeCompleto as nome_aluno
            FROM Comportamento c
            INNER JOIN Aluno a ON c.idAluno = a.idAluno
            WHERE c.idProfessor = %s
            ORDER BY a.nomeCompleto ASC
        """
        cursor.execute(query, (id_professor,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def listar_tags_distintas_professor(id_professor):
    """Busca as tags únicas do professor para preencher o Boxlist."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT tag, MAX(observacao) as observacao 
            FROM Comportamento 
            WHERE idProfessor = %s 
            GROUP BY tag
            ORDER BY tag ASC
        """
        cursor.execute(query, (id_professor,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def salvar_comportamento(tag, observacao, id_aluno, id_professor):
    """Salva um novo registro ou uma nova tag vinculada ao professor."""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO Comportamento (tag, observacao, idAluno, idProfessor) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (tag, observacao, id_aluno, id_professor))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def excluir_comportamento_seguro(id_comp, id_professor):
    """Remove o registro apenas se pertencer ao professor logado."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "DELETE FROM Comportamento WHERE idComportamento = %s AND idProfessor = %s"
        cursor.execute(query, (id_comp, id_professor))
        conn.commit()
        return True
    except: return False
    finally:
        cursor.close()
        conn.close()