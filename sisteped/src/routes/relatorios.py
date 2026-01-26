from flask import Blueprint, render_template, session, redirect, url_for

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('relatorios/relatorios.html', nome=session.get('user_name'))


@relatorios_bp.route('/gerar_relatorio', methods=['GET'])
def gerar_relatorio():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('relatorios/gerar_relatorio.html', nome=session.get('user_name'))