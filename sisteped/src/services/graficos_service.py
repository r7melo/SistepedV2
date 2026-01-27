from .db import get_db_connection

def obter_resumo_comportamento(id_turma):
    """Conta a frequência de cada tag de comportamento para a turma."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.tag, COUNT(c.idComportamento) as total
            FROM Comportamento c
            INNER JOIN Aluno a ON c.idAluno = a.idAluno
            WHERE a.idTurma = %s
            GROUP BY c.tag
        """
        cursor.execute(query, (id_turma,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_timeline_notas(id_turma):
    """Calcula a média mensal das notas da turma para o gráfico de linha."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                DATE_FORMAT(av.data, '%b') as mes,
                AVG(av.nota) as media
            FROM Avaliacao av
            INNER JOIN Aluno a ON av.idAluno = a.idAluno
            WHERE a.idTurma = %s
            GROUP BY MONTH(av.data), mes
            ORDER BY MONTH(av.data)
        """
        cursor.execute(query, (id_turma,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_medias_disciplinas(id_turma):
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        # Extrai o texto entre os últimos parênteses do campo 'conteudo'
        query = """
            SELECT 
                TRIM(REPLACE(SUBSTRING_INDEX(av.conteudo, '(', -1), ')', '')) as disciplina,
                ROUND(AVG(av.nota), 2) as media
            FROM Avaliacao av
            INNER JOIN Aluno a ON av.idAluno = a.idAluno
            WHERE a.idTurma = %s AND av.conteudo LIKE '%(%%)%'
            GROUP BY disciplina
        """
        cursor.execute(query, (id_turma,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_distribuicao_notas(id_turma):
    """Conta quantos alunos estão em cada faixa de nota para o gráfico de barras."""
    conn = get_db_connection()
    if not conn: return [0, 0, 0, 0, 0]
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                SUM(CASE WHEN nota < 3 THEN 1 ELSE 0 END) as '0-3',
                SUM(CASE WHEN nota >= 3 AND nota < 5 THEN 1 ELSE 0 END) as '3-5',
                SUM(CASE WHEN nota >= 5 AND nota < 7 THEN 1 ELSE 0 END) as '5-7',
                SUM(CASE WHEN nota >= 7 AND nota < 9 THEN 1 ELSE 0 END) as '7-9',
                SUM(CASE WHEN nota >= 9 THEN 1 ELSE 0 END) as '9-10'
            FROM Avaliacao av
            INNER JOIN Aluno a ON av.idAluno = a.idAluno
            WHERE a.idTurma = %s
        """
        cursor.execute(query, (id_turma,))
        resultado = cursor.fetchone()
        # Converte None para 0 caso não haja notas
        return [int(x) if x else 0 for x in resultado]
    finally:
        cursor.close()
        conn.close()