# teste_db.py
from modulos.banco.database import session, Cliente

# 1. Inserir um cliente de teste
novo = Cliente(nome="Teste Cliente", telefone="11999999999", email="teste@teste.com", cpf="12345678900")
session.add(novo)
session.commit()
print("✅ Cliente salvo com ID:", novo.id)

# 2. Listar todos os clientes
clientes = session.query(Cliente).all()
print("📋 Clientes cadastrados:")
for c in clientes:
    print(c.id, c.nome, c.telefone, c.email, c.cpf)