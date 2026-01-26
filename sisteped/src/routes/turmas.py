from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from ..services.turma_service import criar_turma, listar_turmas

turmas_bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@turmas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    lista_de_turmas = listar_turmas(session['user_id'])
    
    return render_template('turmas.html', turmas=lista_de_turmas)


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

    return render_template('cadastrar_turma.html')