import csv
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.aluno_service import atualizar_aluno, cadastrar_alunos_em_lote, criar_aluno, deletar_aluno, listar_alunos, obter_aluno_por_id
from ..services.turma_service import listar_turmas

alunos_bp = Blueprint('alunos', __name__, url_prefix='/alunos')


import math

@alunos_bp.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    # Parâmetros da URL
    pagina = request.args.get('pagina', 1, type=int)
    busca = request.args.get('busca', '')
    turma_id = request.args.get('turma_id', 'todos')
    limite = 10 # Alunos por página

    # Chama o service
    alunos, total = listar_alunos(session['user_id'], busca, turma_id, pagina, limite)
    
    # Dados auxiliares para o template
    turmas = listar_turmas(session['user_id'])
    total_paginas = math.ceil(total / limite)

    return render_template('alunos/alunos.html', 
                           alunos=alunos, 
                           turmas=turmas,
                           total_paginas=total_paginas, 
                           pagina_atual=pagina,
                           busca_atual=busca,
                           turma_atual=turma_id)



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


@alunos_bp.route('/importar_csv', methods=['POST'])
def importar_csv():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    arquivo = request.files.get('file')
    id_turma = request.form.get('turma_id')

    if arquivo and arquivo.filename.endswith('.csv'):
        stream = io.StringIO(arquivo.stream.read().decode("UTF-8"), newline=None)
        leitor = csv.DictReader(stream)
        
        total = cadastrar_alunos_em_lote(list(leitor), id_turma)
        
        if total > 0:
            flash(f'Importação concluída: {total} alunos cadastrados!', 'success')
        else:
            flash('Nenhum aluno foi cadastrado. Verifique o arquivo.', 'error')
    else:
        flash('Arquivo inválido. Use o modelo .csv disponível no modal.', 'error')
        
    return redirect(url_for('alunos.index'))