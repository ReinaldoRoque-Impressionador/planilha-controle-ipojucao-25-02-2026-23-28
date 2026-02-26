import csv
from modulos.banco.database import SessionLocal, Cliente, Pets, FotoPet

def resumo_clientes():
    with SessionLocal() as db:
        # Contagens gerais
        total_clientes = db.query(Cliente).count()
        total_pets = db.query(Pets).count()
        total_fotos = db.query(FotoPet).count()

        # Abrir arquivo CSV para salvar resumo
        with open("resumo.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Cabeçalho geral
            writer.writerow(["Resumo do Banco"])
            writer.writerow(["Total de Clientes", total_clientes])
            writer.writerow(["Total de Pets", total_pets])
            writer.writerow(["Total de Fotos", total_fotos])
            writer.writerow([])  # Linha em branco

            # Cabeçalho detalhado
            writer.writerow([
                "Cliente ID", "Nome", "Telefone", "Email", "Endereço", "Número", "Complemento", "Bairro", "Ponto de Referência", "CPF",
                "Pet Nome", "Pet Raça", "Pet Porte",
                "Foto Caminho", "Foto Descrição"
            ])

            clientes = db.query(Cliente).all()
            for cliente in clientes:
                if cliente.pets:
                    for pet in cliente.pets:
                        if pet.fotos:
                            for foto in pet.fotos:
                                writer.writerow([
                                    cliente.id, cliente.nome, cliente.telefone, cliente.email, cliente.endereco, cliente.numero, cliente.complemento, cliente.bairro, cliente.ponto_referencia, cliente.cpf,
                                    pet.nome, pet.raca, pet.porte,
                                    foto.caminho, foto.descricao
                                ])
                        else:
                            writer.writerow([
                                cliente.id, cliente.nome, cliente.telefone, cliente.email, cliente.endereco, cliente.numero, cliente.complemento, cliente.bairro, cliente.ponto_referencia, cliente.cpf,
                                pet.nome, pet.raca, pet.porte,
                                "", ""
                            ])
                else:
                    writer.writerow([
                        cliente.id, cliente.nome, cliente.telefone, cliente.email, cliente.endereco, cliente.numero, cliente.complemento, cliente.bairro, cliente.ponto_referencia, cliente.cpf,
                        "", "", "",
                        "", ""
                    ])

if __name__ == "__main__":
    resumo_clientes()