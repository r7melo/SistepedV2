from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.notas_service import atualizar_nota_individual, listar_alunos_por_turma, listar_notas, listar_turmas, remover_nota_individual, salvar_avaliacao

notas_bp = Blueprint('notas', __name__, url_prefix='/notas')

@notas_bp.route('/', methods=['GET'])
def index():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    notas_brutas = listar_notas(session['user_id'])
    
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

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    id_professor = session['user_id']

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


    turmas_lista = listar_turmas(id_professor)

    turma_selecionada = request.args.get('turma')
    alunos_lista = []

    if turma_selecionada:
        # Busca alunos da turma validando o acesso do professor
        alunos_lista = listar_alunos_por_turma(turma_selecionada, id_professor)

    return render_template('cadastrar_notas.html', turmas=turmas_lista, alunos=alunos_lista, turma_atual=turma_selecionada)


@notas_bp.route('/atualizar_individual/<int:id>', methods=['POST'])
def atualizar_individual(id):
    # Pega a nova nota vinda do input 'nova_nota' do modal
    nova_nota = request.form.get('nova_nota')
    
    if atualizar_nota_individual(id, nova_nota):
        flash('Nota atualizada com sucesso!', 'success')
    else:
        flash('Erro ao atualizar nota.', 'error')
        
    return redirect(url_for('notas.index'))

@notas_bp.route('/excluir_individual/<int:id>')
def excluir_individual(id):
    # Remove apenas o registro específico da tabela Avaliacao
    if remover_nota_individual(id):
        flash('Registro de nota removido!', 'success')
    else:
        flash('Erro ao remover nota.', 'error')
        
    return redirect(url_for('notas.index'))
