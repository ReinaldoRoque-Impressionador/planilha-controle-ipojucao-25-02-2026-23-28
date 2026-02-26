from modulos.banco.database import SessionLocal, Cliente

def listar_clientes():
    with SessionLocal() as db:
        clientes = db.query(Cliente).all()
        for cliente in clientes:
            print(f"👤 Cliente: {cliente.nome} | Email: {cliente.email}")
            for pet in cliente.pets:
                print(f"   🐶 Pet: {pet.nome} | Raça: {pet.raca} | Porte: {pet.porte}")
                for foto in pet.fotos:
                    print(f"      📷 Foto: {foto.caminho} | Descrição: {foto.descricao}")

if __name__ == "__main__":
    listar_clientes()