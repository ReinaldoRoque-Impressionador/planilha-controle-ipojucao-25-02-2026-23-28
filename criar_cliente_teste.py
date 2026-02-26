from modulos.banco.database import SessionLocal, Cliente, Pets, FotoPet

def criar_cliente_teste():
    with SessionLocal() as db:
        cliente = Cliente(
            nome="Maria Silva",
            telefone="11999999999",
            email="maria@exemplo.com",
            endereco="Rua das Flores",
            numero="123",
            complemento="Apto 45",
            bairro="Centro",
            ponto_referencia="Próximo à praça",
            cpf="123.456.789-00"
        )

        pet = Pets(
            nome="Rex",
            raca="Labrador",
            porte="médio",
            cliente=cliente
        )

        foto1 = FotoPet(caminho="rex1.jpg", descricao="Pelagem", pet=pet)
        foto2 = FotoPet(caminho="rex2.jpg", descricao="Vacinação", pet=pet)

        db.add(cliente)
        db.add(pet)
        db.add(foto1)
        db.add(foto2)
        db.commit()

        print("✅ Cliente, PET e Fotos salvos com sucesso!")

if __name__ == "__main__":
    criar_cliente_teste()