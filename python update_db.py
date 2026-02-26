# update_db.py
from sqlalchemy import create_engine, text

# ajuste para o caminho do seu banco
engine = create_engine("sqlite:///modulos/banco/ipojucao.db")

with engine.connect() as conn:
    # adiciona coluna telefone se não existir
    try:
        conn.execute(text("ALTER TABLE clientes ADD COLUMN telefone VARCHAR"))
        print("Coluna 'telefone' adicionada com sucesso.")
    except Exception as e:
        print("Aviso:", e)

    # adiciona coluna email se não existir
    try:
        conn.execute(text("ALTER TABLE clientes ADD COLUMN email VARCHAR"))
        print("Coluna 'email' adicionada com sucesso.")
    except Exception as e:
        print("Aviso:", e)