# database.py

#from flask_sqlalchemy import SQLAlchemy

# Criando instância global que será usada em toda a aplicação
# database = SQLAlchemy()

# modulos/banco/database.py

from sqlalchemy import text

from sqlalchemy import inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import Column, Integer, String
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean, Text, Date, Float

from sqlalchemy.orm import relationship
from modulos.banco import database
from sqlalchemy import Time
from sqlalchemy import DateTime
from datetime import datetime




import os

#from modulos.banco import db_models  # Isso garante que todas as classes estejam registradas

def inserir_usuarios_desenvolvedores():
    from modulos.banco.db_models import Usuario
    db = SessionLocal()

    usuarios_dev = [
        Usuario(nome="Raphael", email="cebous@hotmail.com.br", senha="1234", perfil="dev"),
        Usuario(nome="Reinaldo", email="roquereinaldo@gmail.com", senha="975624asa", perfil="dev")
    ]

    for usuario in usuarios_dev:
        existente = db.query(Usuario).filter_by(email=usuario.email).first()
        if not existente:
            db.add(usuario)

    db.commit()
    db.close()


def usar_sessao():
    from banco.database import SessionLocal  # importação local evita ciclo
    session = SessionLocal()

# Caminho do banco — você pode mudar para uma pasta específica se quiser
# DATABASE_URL = "sqlite:///./modulos/banco/meubanco.db"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "modulos", "banco", "meubanco.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"



# Criação do engine e da sessão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()   # ✅ use "session" para manipular dados



#
# # Base para os modelos
# Base = declarative_base()
#
# session = SessionLocal()

# def inicializar_banco():
#     print("🔄 Criando tabelas...")
#     from modulos.banco import db_models  # ✅ Importa os modelos depois que Base existe




# def inicializar_banco():
#     from sqlalchemy import inspect
#     inspector = inspect(engine)
#     if not inspector.has_table("usuarios"):  # ou qualquer tabela-chave
#         print("🔄 Criando tabelas...")
#         Base.metadata.create_all(bind=engine)
#         print("✅ Banco pronto!")
#     else:
#         print("⚠️ Tabelas já existem. Nenhuma ação necessária.")

# def inicializar_banco():
#     print("🔄 Verificando e criando tabelas...")
#     Base.metadata.create_all(bind=engine)
#     print("✅ Banco pronto!")

def inicializar_banco():
    print("🔄 Verificando e criando tabelas...")
    import modulos.banco.database
    Base.metadata.create_all(bind=engine)
    print("✅ Banco pronto!")



def testar_conexao():
    from sqlalchemy import inspect, text
    from sqlalchemy.exc import SQLAlchemyError
    #from modulos.banco.db_models import Cliente, Pagamento

    try:
        db = SessionLocal()

        # 1. Teste básico com expressão textual correta
        resultado = db.execute(text("SELECT 1"))
        print("✅ Conexão básica OK:", resultado.fetchone())

        # 2. Verificar tabelas existentes
        inspetor = inspect(db.bind)
        tabelas = inspetor.get_table_names()
        print("📋 Tabelas encontradas:", tabelas)

        # 3. Verificar se há dados nas tabelas principais
        cliente_count = db.query(Cliente).count()
        pagamento_count = db.query(Pagamento).count()

        print(f"👤 Clientes cadastrados: {cliente_count}")
        print(f"💳 Pagamentos registrados: {pagamento_count}")

    except SQLAlchemyError as e:
        print("❌ Erro ao conectar ou consultar o banco:")
        print(e)
    finally:
        db.close()





# ALTERADO AQUI  ( ABAIXO )


# === TABELA: CLIENTE ===
class Cliente(Base):
    __tablename__ = 'clientes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    email = Column(String, unique=True)
    cpf = Column(String, unique=False)

    # Endereço detalhado
    endereco = Column(String)  # rua/avenida
    numero = Column(String)  # número da casa/apto
    complemento = Column(String)  # andar, casa 1, casa 2 etc
    bairro = Column(String)  # bairro
    ponto_referencia = Column(String)  # ponto de referência

    foto_cliente = Column(String)  # caminho da imagem

    pets = relationship("Pets", back_populates="cliente")


# === FUNÇÕES CRUD: CLIENTE ===
def salvar_cliente(nome):
    db = SessionLocal()
    novo_cliente = Cliente(nome=nome)
    db.add(novo_cliente)
    try:
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print("Erro ao salvar cliente:", e)
        return False
    finally:
        db.close()

def listar_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return clientes

def atualizar_cliente(id_cliente, novo_nome):
    db = SessionLocal()
    cliente = db.query(Cliente).filter_by(id=id_cliente).first()
    if cliente:
        cliente.nome = novo_nome
        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print("Erro ao atualizar cliente:", e)
    db.close()
    return False

def buscar_clientes(campo, valor):
    db = SessionLocal()
    query = db.query(Cliente)
    if campo == "ID":
        resultado = query.filter(Cliente.id == int(valor)).all()
    elif campo == "CPF":
        resultado = query.filter(Cliente.cpf.like(f"%{valor}%")).all()
    elif campo == "E-mail":
        resultado = query.filter(Cliente.email.like(f"%{valor}%")).all()
    else:
        resultado = []
    db.close()
    return resultado

def excluir_cliente(id_cliente):
    db = SessionLocal()
    cliente = db.query(Cliente).filter_by(id=id_cliente).first()
    if cliente:
        try:
            db.delete(cliente)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print("Erro ao excluir cliente:", e)
    db.close()
    return False





# ALTERADO AQUI ( ACIMA )

# alterado aqui ( abaixo )
class DadosCompartilhados(Base):
    __tablename__ = "dados_compartilhados"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    tipo = Column(String)
    data = Column(Date)

# === TABELA: USUÁRIO (LOGIN) ===
class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    perfil = Column(String, default="usuario")  # Pode ser "usuario", "admin", "dev"

# === TABELA: TUTOR ===
class Tutor(Base):
    __tablename__ = 'tutores'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    email = Column(String, unique=True)
    endereco = Column(String)
    numero = Column(String)
    complemento = Column(String)
    data_cadastro = Column(DateTime, default=datetime.now)


    #pets = relationship("modulos.modelos.pets_model.Pets", back_populates='tutor')
    #pets = relationship("Pets", back_populates='tutor')
    #pets = relationship("modulos.modelos.pets_model.Pets", back_populates='tutor')


# === TABELA: PET ===
class Pets(Base):
    __tablename__ = 'pets'
    __table_args__ = {'extend_existing': True}
    #__module__ = 'modulos.banco.models.pets'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    cliente = relationship('Cliente', back_populates='pets')

    idade_anos = Column(String)
    idade_meses = Column(String)
    porte = Column(String) # armazenado como texto, mas na interface é Combobox
    raca = Column(String)  # idem - (acima)
    descricao_pelagem = Column(String)
    fotos = relationship("FotoPet", back_populates="pet", cascade="all, delete-orphan")
    foto = Column(String, default='default.jpg')

    # Novos campos
    problemas_pele = Column(Boolean, default=False)
    problemas_saude = Column(Boolean, default=False)
    descricao_saude = Column(String)  # texto livre
    shampoo_terapeutico = Column(Boolean, default=False)
    hidratante_terapeutico = Column(Boolean, default=False)
    outras_info = Column(Boolean, default=False)
    descricao_outras_info = Column(String)  # texto livre

    atendimentos = relationship('Atendimento', back_populates='pet')
    # tutor_id = Column(Integer, ForeignKey('tutores.id'), nullable=False)
    # tutor = relationship('Tutor', back_populates='pets')

class FotoPet(Base):
    __tablename__ = "fotos_pets"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    caminho = Column(String, nullable=False)   # caminho da imagem
    descricao = Column(String)                 # ex: "Pelagem", "Vacinação"

    pet = relationship("Pets", back_populates="fotos")


# === TABELA: ATENDIMENTO ===
class Atendimento(Base):
    __tablename__ = 'atendimentos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    data_hora_servico = Column(DateTime, nullable=False, default=datetime.now)
    #horario_servico = Column(Time, nullable=False) # novo campo
    servicos_realizados = Column(String)

    # Radiobuttons

    observacoes = Column(String)

    # Novos campos para condições do PET (radiobuttons)
    pode_usar_secador = Column(Boolean, default=False)
    pode_usar_soprador = Column(Boolean, default=False)
    uso_perfume = Column(String)  # valores: "sim", "não", "pouco"
    pode_usar_aderecos = Column(Boolean, default=False)

    observacoes = Column(String)

    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    pet = relationship("Pets", back_populates='atendimentos')
    pagamento = relationship('Pagamento', back_populates='atendimento', uselist=False)

    # servicos_real
# === TABELA: PAGAMENTO ===
class Pagamento(Base):
    __tablename__ = 'pagamentos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    forma_pagamento = Column(String)
    valor_total = Column(Float, nullable=False)
    desconto_fixo = Column(Float, default=0)
    desconto_percentual = Column(Float, default=0)
    data_pagamento = Column(Date)

    atendimento_id = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    atendimento = relationship('Atendimento', back_populates='pagamento')



# alterado aqui ( acima )




# def testar_conexao():
#     from sqlalchemy.exc import SQLAlchemyError
#
#     try:
#         db = SessionLocal()
#         resultado = db.execute("SELECT 1")
#         print("✅ Conexão com o banco de dados bem-sucedida!")
#         print("Resultado:", resultado.fetchone())
#     except SQLAlchemyError as e:
#         print("❌ Erro ao conectar com o banco de dados:")
#         print(e)
#     finally:
#         db.close()