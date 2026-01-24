import sys
import os

# Adiciona o diretório pai ao path para conseguir importar 'routes' e 'services'
# Isso resolve o problema de imports quando as pastas estão lado a lado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__, 
            template_folder='../templates',  # Aponta para a pasta irmã
            static_folder='../static')       # Aponta para a pasta irmã

# Chave secreta necessária para usar Sessão
app.secret_key = 'chave_super_secreta_do_sisteped'

# Registra as rotas
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)