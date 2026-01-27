import csv
import io
from flask import Blueprint, render_template, session, redirect, url_for, request, Response
from ..services.disciplina_service import listar_disciplinas_por_professor
from ..services.relatorios_service import buscar_dados_notas
from ..services.notas_service import listar_turmas

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    id_prof = session['user_id']
    
    return render_template('relatorios/relatorio.html', 
                           turmas=listar_turmas(id_prof),
                           disciplinas=listar_disciplinas_por_professor(id_prof))

@relatorios_bp.route('/exportar', methods=['POST'])
def exportar():
    if 'user_id' not in session: return redirect(url_for('auth.login'))

    id_turma = request.form.get('turma')
    disciplina = request.form.get('disciplina')
    d_inicio = request.form.get('data_inicio')
    d_fim = request.form.get('data_fim')
    
    # Busca os dados no banco
    dados = buscar_dados_notas(session['user_id'], id_turma, disciplina, d_inicio, d_fim)

    # Criação do CSV em memória
    output = io.StringIO()
    output.write(u'\ufeff') # Garante acentuação correta no Excel
    writer = csv.writer(output, delimiter=';')

    # Cabeçalho da planilha
    writer.writerow(['Aluno', 'Avaliação (Conteúdo)', 'Nota', 'Data'])

    # Linhas de dados
    for d in dados:
        # Converte ponto em vírgula para as notas (padrão Brasil no Excel)
        nota_formatada = str(d['nota']).replace('.', ',')
        writer.writerow([d['aluno'], d['conteudo'], nota_formatada, d['data_formatada']])

    output.seek(0)
    filename = f"notas_{disciplina}_{id_turma}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )