from .db import get_db_connection

def listar_comportamentos_professor(id_professor, busca='', tag='todas', pagina=1, limite=10):
    """Lista os registros de comportamento com paginação e filtros."""
    conn = get_db_connection()
    if not conn: return [], 0
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Calcular o deslocamento (offset)
        offset = (pagina - 1) * limite
        
        # 2. Base da Query de Dados
        query = """
            SELECT c.idComportamento, c.tag, c.observacao, a.nomeCompleto as nome_aluno
            FROM Comportamento c
            INNER JOIN Aluno a ON c.idAluno = a.idAluno
            WHERE c.idProfessor = %s
        """
        params = [id_professor]

        if busca:
            query += " AND a.nomeCompleto LIKE %s"
            params.append(f"%{busca}%")

        if tag and tag != 'todas' and tag != 'None':
            query += " AND c.tag = %s"
            params.append(tag)

        # Query para pegar o TOTAL de registros sem o limite (para a paginação)
        query_total = f"SELECT COUNT(*) as total FROM ({query}) as sub"
        
        # Adicionar ordenação e limites à query de dados
        query += " ORDER BY a.nomeCompleto ASC LIMIT %s OFFSET %s"
        params_dados = params + [limite, offset]
        
        # Executar busca do total
        cursor.execute(query_total, tuple(params))
        total_registros = cursor.fetchone()['total']
        
        # Executar busca dos dados paginados
        cursor.execute(query, tuple(params_dados))
        registros = cursor.fetchall()
        
        return registros, total_registros

    except Exception as e:
        print(f"Erro ao listar comportamentos: {e}")
        return [], 0
    finally:
        if conn and conn.is_connected():
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