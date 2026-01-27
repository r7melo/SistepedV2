from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from ..services.turma_service import listar_turmas
from ..services.graficos_service import (
    obter_resumo_comportamento, 
    obter_timeline_notas, 
    obter_medias_disciplinas, 
    obter_distribuicao_notas
)

graficos_bp = Blueprint('graficos', __name__, url_prefix='/graficos')

@graficos_bp.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    turmas = listar_turmas(session['user_id'])
    return render_template('graficos/graficos.html', turmas=turmas)

# Endpoints de API para o JavaScript
@graficos_bp.route('/api/comportamento/<int:turma_id>')
def api_comportamento(turma_id):
    dados = obter_resumo_comportamento(turma_id)
    return jsonify(dados)

@graficos_bp.route('/api/timeline/<int:turma_id>')
def api_timeline(turma_id):
    dados = obter_timeline_notas(turma_id)
    return jsonify(dados)

@graficos_bp.route('/api/disciplinas/<int:turma_id>')
def api_disciplinas(turma_id):
    dados = obter_medias_disciplinas(turma_id)
    return jsonify(dados)

@graficos_bp.route('/api/distribuicao/<int:turma_id>')
def api_distribuicao(turma_id):
    dados = obter_distribuicao_notas(turma_id)
    return jsonify(dados)