from flask import Flask
from .routes.auth import auth_bp
from .routes.graficos import graficos_bp
from .routes.relatorios import relatorios_bp
from .routes.alunos import alunos_bp
from .routes.notas import notas_bp
from .routes.turmas import turmas_bp

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static'
)

# Chave secreta (SHA256 Hash)
app.secret_key = '0449d692ab7e1a825e80abb1c3e6c1fcd716567ecf5cc858ce2ff5dcbddda50d'

# Registrar rotas
app.register_blueprint(auth_bp)
app.register_blueprint(graficos_bp)
app.register_blueprint(relatorios_bp)
app.register_blueprint(alunos_bp)
app.register_blueprint(notas_bp)
app.register_blueprint(turmas_bp)
