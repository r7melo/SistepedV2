from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.routes import turmas
from src.services.comportamento_service import excluir_comportamento_seguro, listar_comportamentos_professor, listar_tags_distintas_professor, salvar_comportamento
from src.services.turma_service import listar_turmas
from ..services.aluno_service import listar_alunos

comportamento_bp = Blueprint('comportamento', __name__, url_prefix='/comportamento')

@comportamento_bp.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    busca = request.args.get('busca', '')
    tag = request.args.get('tag', 'todas')

    id_prof = session['user_id']
    comportamentos = listar_comportamentos_professor(id_prof, busca, tag)
    turmas = listar_turmas(id_prof)
    tags_existentes = listar_tags_distintas_professor(id_prof)
    alunos = listar_alunos(id_prof)
    
    return render_template('comportamento/comportamento.html', 
                           comportamentos=comportamentos, 
                           tags_existentes=tags_existentes,
                           alunos=alunos,
                           busca_atual=busca,
                           turmas=turmas,
                           tag_atual=tag)

@comportamento_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    id_prof = session['user_id']
    id_aluno = request.form.get('id_aluno')
    modo_escrita = request.form.get('modo_escrita') == 'true'
    
    if modo_escrita:
        tag = request.form.get('tag_nova')
        observacao = request.form.get('observacao')
    else:
        tag = request.form.get('tag_existente')
        observacao = request.form.get('observacao')

    if salvar_comportamento(tag, observacao, id_aluno, id_prof):
        flash('Registro de comportamento salvo!', 'success')
    else:
        flash('Erro ao salvar registro.', 'error')
        
    return redirect(url_for('comportamento.index'))

@comportamento_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    if excluir_comportamento_seguro(id, session['user_id']):
        flash('Registro removido!', 'success')
    return redirect(url_for('comportamento.index'))