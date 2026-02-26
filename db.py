# # db.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# DATABASE_URL = "sqlite:///banco.db"
#
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()








# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# # Criação do engine com SQLite
# engine = create_engine('sqlite:///ipojucadb.db', echo=True)
#
# # Classe base para os modelos
# Base = declarative_base()
#
# # Criador de sessões
# SessionLocal = sessionmaker(bind=engine)

#1.  — configura o banco de dados
# Esse arquivo centraliza a conexão com o banco de dados

