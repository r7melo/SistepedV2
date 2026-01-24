from flask import Flask
from .routes.auth import auth_bp

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

# Chave secreta
app.secret_key = 'chave_super_secreta_do_sisteped'

# Registrar blueprints / rotas
app.register_blueprint(auth_bp)