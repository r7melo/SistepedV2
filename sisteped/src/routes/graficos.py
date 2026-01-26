from flask import Blueprint, render_template, session, redirect, url_for

graficos_bp = Blueprint('graficos', __name__, url_prefix='/graficos')

@graficos_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('graficos/graficos.html', nome=session.get('user_name'))