from .db import get_db_connection

def buscar_dados_notas(id_professor, id_turma, disciplina_nome, data_inicio, data_fim):
    """Busca o histórico de notas filtrado por turma, disciplina e datas."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        # Filtramos pela Turma do aluno e verificamos se o professor tem acesso a essa turma
        query = """
            SELECT 
                a.nomeCompleto as aluno, 
                av.conteudo, 
                av.nota, 
                DATE_FORMAT(av.data, '%d/%m/%Y') as data_formatada
            FROM Avaliacao av
            INNER JOIN Aluno a ON av.idAluno = a.idAluno
            INNER JOIN ProfessorTurma pt ON a.idTurma = pt.idTurma
            WHERE pt.idProfessor = %s 
              AND a.idTurma = %s
              AND av.conteudo LIKE %s
              AND av.data BETWEEN %s AND %s
            ORDER BY a.nomeCompleto ASC, av.data ASC
        """
        # Formata o filtro: ex: '%(Matemática)%'
        filtro_disciplina = f"%({disciplina_nome})%"
        cursor.execute(query, (id_professor, id_turma, filtro_disciplina, data_inicio, data_fim))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()