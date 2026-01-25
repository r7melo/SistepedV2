from .db import get_db_connection

def criar_aluno(dados):
    conn = get_db_connection()
    if not conn: return False

    try:
        cursor = conn.cursor()
        
        filiacao_completa = f"Pai: {dados['nome_pai']} | Mãe: {dados['nome_mae']}"

        query_aluno = """
            INSERT INTO Aluno (nomeCompleto, cpf, identidade, filiacao, idTurma) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_aluno, (
            dados['nome'], 
            dados['cpf'], 
            dados['identidade'], 
            filiacao_completa,
            None
        ))
        
        id_novo_aluno = cursor.lastrowid

        if dados['email'] or dados['telefone']:
            query_contato = "INSERT INTO Contato (email, telefone, idAluno) VALUES (%s, %s, %s)"
            cursor.execute(query_contato, (dados['email'], dados['telefone'], id_novo_aluno))

        conn.commit()
        return True

    except Exception as e:
        print(f"Erro ao criar aluno: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()