from .db import get_db_connection

def criar_aluno(dados):
    """
    Recebe um dicionário com os dados do formulário e salva no banco.
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        pai = dados.get('nome_pai', '')
        mae = dados.get('nome_mae', '')
        filiacao = f"Pai: {pai} | Mãe: {mae}"

        query_aluno = """
            INSERT INTO Aluno (nomeCompleto, cpf, identidade, filiacao, idTurma)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_aluno, (
            dados['nome'], 
            dados['cpf'], 
            dados['identidade'], 
            filiacao, 
            dados['turma_id']
        ))
        
        id_novo_aluno = cursor.lastrowid

        if dados.get('email') or dados.get('telefone'):
            query_contato = """
                INSERT INTO Contato (email, telefone, idAluno)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_contato, (dados['email'], dados['telefone'], id_novo_aluno))

        conn.commit()
        return True

    except Exception as e:
        print(f"Erro ao criar aluno: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def listar_alunos(id_professor, termo_busca=None, id_turma=None):
    conn = get_db_connection()
    resultados = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Base da Query
            query = """
                SELECT a.idAluno, a.nomeCompleto, a.cpf, t.nome AS nome_turma, t.idTurma
                FROM Aluno a
                INNER JOIN Turma t ON a.idTurma = t.idTurma
                INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
                WHERE pt.idProfessor = %s
            """
            params = [id_professor]

            # Filtro por Nome
            if termo_busca:
                query += " AND a.nomeCompleto LIKE %s"
                params.append(f"%{termo_busca}%")

            # Filtro por Turma
            if id_turma and id_turma != 'todos':
                query += " AND t.idTurma = %s"
                params.append(id_turma)

            query += " ORDER BY a.nomeCompleto ASC"
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return resultados


def obter_aluno_por_id(id_aluno):
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                a.idAluno, 
                a.nomeCompleto, 
                a.cpf, 
                a.identidade, 
                a.filiacao, 
                a.idTurma,
                c.email AS contato_email, 
                c.telefone AS contato_tel,
                t.nome AS nomeTurma
            FROM Aluno a
            LEFT JOIN Contato c ON a.idAluno = c.idAluno
            LEFT JOIN Turma t ON a.idTurma = t.idTurma
            WHERE a.idAluno = %s
            LIMIT 1
        """
        
        cursor.execute(query, (id_aluno,))
        aluno_db = cursor.fetchone()
        
        if not aluno_db:
            return None

        filiacao_bruta = aluno_db.get('filiacao') or ""
        pai, mae = "", ""
        
        if "|" in filiacao_bruta:
            partes = filiacao_bruta.split("|")
            pai = partes[0].replace("Pai:", "").strip()
            mae = partes[1].replace("Mãe:", "").strip()
        elif " e " in filiacao_bruta:
            partes = filiacao_bruta.split(" e ", 1)
            pai = partes[0].strip()
            mae = partes[1].strip()
        else:
            pai = filiacao_bruta.strip()

        aluno_para_html = {
            'idAluno': aluno_db['idAluno'],
            'nome': aluno_db['nomeCompleto'],       
            'cpf': aluno_db.get('cpf') or "",
            'identidade': aluno_db.get('identidade') or "",
            'nome_pai': pai,                        
            'nome_mae': mae,                        
            'email': aluno_db.get('contato_email') or "",
            'telefone': aluno_db.get('contato_tel') or "", 
            'idTurma': aluno_db['idTurma'],
            'nomeTurma': aluno_db.get('nomeTurma') or "Sem Turma"
        }

        return aluno_para_html
    finally:
        cursor.close()
        conn.close()

def atualizar_aluno(id_aluno, dados):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        
        filiacao_junta = f"Pai: {dados['nome_pai']} | Mãe: {dados['nome_mae']}"
        
        query_aluno = """
            UPDATE Aluno 
            SET nomeCompleto = %s, cpf = %s, identidade = %s, filiacao = %s, idTurma = %s
            WHERE idAluno = %s
        """
        cursor.execute(query_aluno, (
            dados['nome'], dados['cpf'], dados['identidade'], filiacao_junta, dados['turma_id'], id_aluno
        ))

        cursor.execute("SELECT idContato FROM Contato WHERE idAluno = %s", (id_aluno,))
        contato_existente = cursor.fetchone()

        if contato_existente:
            query_contato = "UPDATE Contato SET email = %s, telefone = %s WHERE idAluno = %s"
            cursor.execute(query_contato, (dados['email'], dados['telefone'], id_aluno))
        else:
            query_contato = "INSERT INTO Contato (email, telefone, idAluno) VALUES (%s, %s, %s)"
            cursor.execute(query_contato, (dados['email'], dados['telefone'], id_aluno))

        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def deletar_aluno(id_aluno):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        
        # 1. Apagar registros vinculados
        cursor.execute("DELETE FROM Contato WHERE idAluno = %s", (id_aluno,))
        cursor.execute("DELETE FROM Endereco WHERE idAluno = %s", (id_aluno,))
        cursor.execute("DELETE FROM Avaliacao WHERE idAluno = %s", (id_aluno,))
        cursor.execute("DELETE FROM Comportamento WHERE idAluno = %s", (id_aluno,))
        
        # 2. Apagar Aluno
        cursor.execute("DELETE FROM Aluno WHERE idAluno = %s", (id_aluno,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar aluno {id_aluno}: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def cadastrar_alunos_em_lote(lista_csv, id_turma):
    """Percorre a lista do CSV e chama a sua função criar_aluno para cada um."""
    sucessos = 0
    for linha in lista_csv:
        dados_aluno = {
            'nome': linha.get('nome_completo'),
            'cpf': linha.get('cpf'),
            'identidade': linha.get('identidade'),
            'nome_pai': linha.get('nome_pai'),
            'nome_mae': linha.get('nome_mae'),
            'email': linha.get('email'),
            'telefone': linha.get('telefone'),
            'turma_id': id_turma
        }
        if criar_aluno(dados_aluno):
            sucessos += 1
    return sucessos