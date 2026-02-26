from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "modulos", "banco", "meubanco.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE clientes ADD COLUMN telefone VARCHAR"))
        print("✅ Coluna 'telefone' adicionada com sucesso.")
    except Exception as e:
        print("⚠️ Aviso:", e)



with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE clientes ADD COLUMN endereco TEXT"))
        conn.execute(text("ALTER TABLE clientes ADD COLUMN numero TEXT"))
        conn.execute(text("ALTER TABLE clientes ADD COLUMN complemento TEXT"))
        conn.execute(text("ALTER TABLE clientes ADD COLUMN bairro TEXT"))
        conn.execute(text("ALTER TABLE clientes ADD COLUMN ponto_referencia TEXT"))
        conn.execute(text("ALTER TABLE clientes ADD COLUMN foto_cliente TEXT"))
        print("✅ Todas as colunas adicionadas com sucesso.")
    except Exception as e:
        print("⚠️ Aviso:", e)