from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.notas_service import listar_alunos_por_turma, listar_notas, listar_turmas, salvar_avaliacao

notas_bp = Blueprint('notas', __name__, url_prefix='/notas')

@notas_bp.route('/', methods=['GET'])
def index():
    notas_brutas = listar_notas()
    
    for n in notas_brutas:
        conteudo = n.get('conteudo', '')
        if '(' in conteudo and conteudo.endswith(')'):
            partes = conteudo.rsplit('(', 1)
            n['atividade'] = partes[0].strip()
            n['disciplina'] = partes[1].replace(')', '').strip()
        else:
            n['atividade'] = conteudo
            n['disciplina'] = 'Geral'

    return render_template('notas.html', notas=notas_brutas)

@notas_bp.route('/cadastrar_notas', methods=['GET', 'POST'])
def cadastrar_notas():
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        data = request.form.get('data')
        disciplina = request.form.get('disciplina')
        turma_id = request.form.get('turma')

        notas_salvas = 0

        for key, value in request.form.items():
            
            if key.startswith('nota_'):
                if value and value.strip():
                    id_aluno = key.split('_')[1]
                    nota = value
                    
                    if salvar_avaliacao(titulo, disciplina, data, id_aluno, nota):
                        notas_salvas += 1
        
        if notas_salvas > 0:
            flash(f'Sucesso! {notas_salvas} notas foram lançadas.', 'success')
        else:
            flash('Nenhuma nota foi preenchida. Nada foi salvo.', 'warning')

        return redirect(url_for('notas.cadastrar_notas', turma=turma_id))

    turmas_lista = listar_turmas()

    turma_selecionada = request.args.get('turma')
    alunos_lista = []

    if turma_selecionada:
        alunos_lista = listar_alunos_por_turma(turma_selecionada)

    return render_template('cadastrar_notas.html', 
                           turmas=turmas_lista,
                           alunos=alunos_lista, 
                           turma_atual=turma_selecionada)
