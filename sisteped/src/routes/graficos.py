from flask import Blueprint, render_template, session, redirect, url_for, request
from ..services.turma_service import listar_turmas
from ..services.graficos_service import buscar_dados_dashboard

graficos_bp = Blueprint('graficos', __name__, url_prefix='/graficos')

@graficos_bp.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    id_professor = session['user_id']
    turma_id = request.args.get('turma')
    
    turmas = listar_turmas(id_professor)
    dados = None
    
    if turma_id:
        dados = buscar_dados_dashboard(turma_id)
    
    return render_template('graficos/graficos.html', 
                           turmas=turmas, 
                           turma_id=turma_id, 
                           dados=dados)