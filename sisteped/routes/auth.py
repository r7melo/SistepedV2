from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import validar_usuario

# Criando o Blueprint (grupo de rotas)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    # Se já estiver logado, manda pro menu
    if 'user_id' in session:
        return redirect(url_for('auth.menu'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        senha = request.form.get('password')

        # Chama o serviço para verificar no banco
        usuario = validar_usuario(email, senha)

        if usuario:
            # Salva na sessão (cookie seguro do Flask)
            session['user_id'] = usuario['Id']
            session['user_name'] = usuario['Name']
            session['user_role'] = usuario['Role']
            return redirect(url_for('auth.menu'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html')

@auth_bp.route('/menu')
def menu():
    # Protege a rota: só entra se tiver logado
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('menu.html', nome=session['user_name'])

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))