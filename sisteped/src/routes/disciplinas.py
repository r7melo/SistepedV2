from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.disciplina_service import (
    listar_disciplinas_por_professor, 
    criar_disciplina_com_vinculo, 
    deletar_disciplina_seguro
)

disciplinas_bp = Blueprint('disciplinas', __name__, url_prefix='/disciplinas')

@disciplinas_bp.route('/')
def index():
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    # Filtra as disciplinas pelo professor logado
    lista = listar_disciplinas_por_professor(session['user_id'])
    return render_template('disciplinas/disciplinas.html', disciplinas=lista)

@disciplinas_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    nome = request.form.get('nome')
    if nome:
        # Passa o ID do professor para criar o vínculo
        if criar_disciplina_com_vinculo(nome, session['user_id']):
            flash('Disciplina vinculada com sucesso!', 'success')
        else:
            flash('Erro ao adicionar disciplina.', 'error')
    
    return redirect(url_for('disciplinas.index'))

@disciplinas_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    # Só permite excluir se o vínculo pertencer ao professor logado
    if deletar_disciplina_seguro(id, session['user_id']):
        flash('Disciplina removida!', 'success')
    else:
        flash('Erro ao excluir ou permissão negada.', 'error')
        
    return redirect(url_for('disciplinas.index'))