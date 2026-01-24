from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..services.auth_service import validar_usuario
from ..services.auth_service import validar_usuario, criar_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('auth.menu'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        senha = request.form.get('password')

        usuario = validar_usuario(email, senha)

        if usuario:
            session['user_id'] = usuario['Id']
            session['user_name'] = usuario['Name']
            session['user_role'] = usuario['Role']
            return redirect(url_for('auth.menu'))
        else:
            flash('Usuário ou senha incorretos!', 'error')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('password')
        confirmar_senha = request.form.get('confirm_password')

        if senha != confirmar_senha:
            flash('As senhas não coincidem!', 'error')
            return render_template('register.html')

        sucesso, mensagem = criar_usuario(nome, email, senha)

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(mensagem, 'error')

    return render_template('register.html')

@auth_bp.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('menu.html', nome=session['user_name'])

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))