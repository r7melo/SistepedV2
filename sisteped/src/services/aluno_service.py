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

def listar_alunos(id_professor):
    """
    Lista apenas os alunos que pertencem a turmas 
    vinculadas ao professor logado através da tabela ProfessorTurma.
    """
    conn = get_db_connection()
    resultados = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
 
            query = """
                SELECT 
                    a.idAluno, 
                    a.nomeCompleto, 
                    a.cpf, 
                    t.nome AS nome_turma
                FROM Aluno a
                INNER JOIN Turma t ON a.idTurma = t.idTurma
                INNER JOIN ProfessorTurma pt ON t.idTurma = pt.idTurma
                WHERE pt.idProfessor = %s
                ORDER BY a.nomeCompleto ASC
            """
            cursor.execute(query, (id_professor,))
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar alunos: {e}")
        finally:
            cursor.close()
            conn.close()
    return resultados