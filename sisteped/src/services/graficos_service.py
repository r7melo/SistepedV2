from .db import get_db_connection

def buscar_dados_dashboard(id_turma):
    conn = get_db_connection()
    if not conn: return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Evolução Temporal (Média por Mês)
        query_timeline = """
            SELECT MONTH(av.data) as mes_num, MONTHNAME(av.data) as mes, AVG(av.nota) as media 
            FROM Avaliacao av
            JOIN Aluno al ON av.idAluno = al.idAluno
            WHERE al.idTurma = %s 
            GROUP BY mes_num, mes ORDER BY mes_num
        """
        cursor.execute(query_timeline, (id_turma,))
        timeline = cursor.fetchall()

        # 2. Média por Disciplina
        query_disciplinas = """
            SELECT 
                CASE 
                    WHEN conteudo LIKE '%(%)%' THEN SUBSTRING_INDEX(SUBSTRING_INDEX(conteudo, '(', -1), ')', 1)
                    ELSE 'Geral'
                END as disciplina, 
                AVG(nota) as media
            FROM Avaliacao av
            JOIN Aluno al ON av.idAluno = al.idAluno
            WHERE al.idTurma = %s
            GROUP BY disciplina
        """
        cursor.execute(query_disciplinas, (id_turma,))
        disciplinas = cursor.fetchall()

        # 3. Perfil Comportamental (Contagem Garantida de 10 Pontos)
        tags_fixas = [
            'Participação', 'Foco', 'Colaboração', 'Pontualidade', 'Autonomia', 
            'Respeito', 'Iniciativa', 'Organização', 'Interesse', 'Comunicação'
        ]
        
        query_comp = """
            SELECT tag, COUNT(*) as total 
            FROM Comportamento 
            WHERE idAluno IN (SELECT idAluno FROM Aluno WHERE idTurma = %s)
            GROUP BY tag
        """
        cursor.execute(query_comp, (id_turma,))
        resultados_comp = {row['tag']: row['total'] for row in cursor.fetchall()}

        # Montamos a lista final garantindo a ordem e os zeros
        comportamento_final = []
        for tag in tags_fixas:
            comportamento_final.append({
                'tag': tag,
                'total': resultados_comp.get(tag, 0)
            })

        # 4. Distribuição de Notas (Histograma)
        cursor.execute("SELECT nota FROM Avaliacao av JOIN Aluno al ON av.idAluno = al.idAluno WHERE al.idTurma = %s", (id_turma,))
        notas = [float(row['nota']) for row in cursor.fetchall()]
        dist = [0, 0, 0, 0, 0]
        for n in notas:
            if n < 3: dist[0]+=1
            elif n < 5: dist[1]+=1
            elif n < 7: dist[2]+=1
            elif n < 9: dist[3]+=1
            else: dist[4]+=1

        return {
            "timeline": timeline,
            "disciplinas": disciplinas,
            "comportamento": comportamento_final,
            "distribuicao": dist
        }
    except Exception as e:
        print(f"Erro no Dashboard: {e}")
        return None
    finally:
        cursor.close()
        conn.close()