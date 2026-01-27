from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from ..services.turma_service import atualizar_turma, criar_turma, deletar_turma, listar_turmas, obter_turma_por_id

turmas_bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@turmas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    busca = request.args.get('busca', '')
    lista_de_turmas = listar_turmas(session['user_id'], busca)

    return render_template('turmas/turmas.html', turmas=lista_de_turmas, busca_atual=busca)


@turmas_bp.route('/cadastrar_turma', methods=['GET', 'POST'])
def cadastrar_turma():
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        ano = request.form.get('ano')
        
        if criar_turma(nome, ano, session['user_id']):
            flash('Turma criada com sucesso!', 'success')
            return redirect(url_for('turmas.index'))
        else:
            flash('Erro ao criar turma.', 'error')

    return render_template('turmas/cadastrar_turma.html')

@turmas_bp.route('/editar_turma/<int:id>', methods=['GET', 'POST'])
def editar_turma(id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    id_professor = session['user_id']
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        ano = request.form.get('ano')
        
        if atualizar_turma(id, nome, ano):
            flash('Turma atualizada com sucesso!', 'success')
            return redirect(url_for('turmas.index'))
        else:
            flash('Erro ao atualizar turma.', 'error')

    turma = obter_turma_por_id(id, id_professor)
    if not turma:
        return redirect(url_for('turmas.index'))

    return render_template('turmas/editar_turma.html', turma=turma)

@turmas_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_turma(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if deletar_turma(id, session['user_id']):
        flash('Turma removida com sucesso.', 'success')
    else:
        flash('Erro ao excluir. Verifique se há alunos vinculados.', 'error')
        
    return redirect(url_for('turmas.index'))