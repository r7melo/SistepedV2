from flask import Blueprint, render_template, session, redirect, url_for

turmas_bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@turmas_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('turmas.html', nome=session.get('user_name'))