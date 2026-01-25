from flask import Blueprint, render_template, session, redirect, url_for

alunos_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@alunos_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('alunos.html', nome=session.get('user_name'))