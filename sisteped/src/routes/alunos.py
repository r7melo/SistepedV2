from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.aluno_service import atualizar_aluno, criar_aluno, deletar_aluno, listar_alunos, obter_aluno_por_id
from ..services.turma_service import listar_turmas

alunos_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@alunos_bp.route('/', methods=['GET'])
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    lista_alunos = listar_alunos(session['user_id'])
    
    return render_template('alunos/alunos.html', alunos=lista_alunos)

@alunos_bp.route('/cadastrar_aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        dados_aluno = {
            'nome': request.form.get('nome'),
            'turma_id': request.form.get('turma_id'),
            'cpf': request.form.get('cpf'),
            'identidade': request.form.get('identidade'),
            'nome_pai': request.form.get('nome_pai'),
            'nome_mae': request.form.get('nome_mae'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone')
        }

        if criar_aluno(dados_aluno):
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('alunos.cadastrar_aluno'))
        else:
            flash('Erro ao cadastrar aluno. Verifique os dados.', 'error')

    lista_turmas = listar_turmas(session['user_id'])
    
    return render_template('alunos/cadastrar_aluno.html', turmas=lista_turmas)


@alunos_bp.route('/editar_aluno/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    if request.method == 'POST':
        dados = {
            'nome': request.form.get('nome'),
            'turma_id': request.form.get('turma_id'),
            'cpf': request.form.get('cpf'),
            'identidade': request.form.get('identidade'),
            'nome_pai': request.form.get('nome_pai'),
            'nome_mae': request.form.get('nome_mae'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone')
        }
        
        if atualizar_aluno(id, dados):
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('alunos.index'))
        else:
            flash('Erro ao salvar alterações.', 'error')
    
    aluno = obter_aluno_por_id(id)
    lista_turmas = listar_turmas(session['user_id'])
    return render_template('alunos/editar_aluno.html', aluno=aluno, turmas=lista_turmas)

@alunos_bp.route('/excluir_aluno/<int:id>', methods=['POST'])
def excluir_aluno(id):
    if deletar_aluno(id):
        flash('Aluno removido permanentemente.', 'success')
    else:
        flash('Erro ao remover aluno. Verifique dependências.', 'error')
    return redirect(url_for('alunos.index'))