from flask import Blueprint, render_template, session, redirect, url_for

notas_bp = Blueprint('notas', __name__, url_prefix='/notas')

@notas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('notas.html', nome=session.get('user_name'))


@notas_bp.route('/cadastrar_notas', methods=['GET'])
def cadastrar_notas():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('cadastrar_notas.html', nome=session.get('user_name'))