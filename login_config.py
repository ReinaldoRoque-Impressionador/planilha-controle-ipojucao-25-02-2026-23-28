from flask_login import LoginManager
login_manager = LoginManager()
from flask_login import LoginManager

print("Importação bem-sucedida!")

def verificar_credenciais(usuario, senha):
    # Exemplo simples de verificação
    return usuario == "admin" and senha == "1234"