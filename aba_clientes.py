# Versão alternativa da aba de clientes — revisar integração com aba_cadastro.py
import tkinter as tk

from tkinter import ttk, messagebox
import json
import os
from tkinter import filedialog

from abas.aba_config import var_raca
from modulos.recursos import dados_compartilhados as dc

# Banco de dados
#from modulos.banco.db_models import Tutor
from modulos.banco.database import Cliente, Tutor, Usuario, Pagamento, Pets
#dc.inicializar_variaveis(master)
# Cliente
from modulos.recursos.cliente_utils import (salvar_ou_atualizar_cliente, buscar_clientes_por_nome, excluir_cliente_por_id)

# Recursos visuais e sonoros
from modulos.recursos.som_expressao import som_e_expressao_acao

from modulos.recursos.som import tocar_som, tocar_som_curto, parar_som, alternar_som, continuar_som
from modulos.recursos.dados_compartilhados import caminho_arquivo
from modulos.banco import database
from tkinter import filedialog
from PIL import Image, ImageTk

from modulos.banco.database import session, Cliente
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Date, Float

# Interface

# Dados compartilhados
#from modulos.recursos.dados_compartilhados import usuarios,from modulos.recursos import dados_compartilhados as dc config_global, carregar_dados


# . Importações específicas por aba ( aba_cadastro, aba_clientes, aba_consulta) - acima
from modulos.banco.database import testar_conexao
from modulos.recursos.conexao_utils import conexao_valida
from modulos.recursos.dados_compartilhados import dados_pet
from modulos.recursos.dados_compartilhados import imagens_racas, imagens_portes, dados_pet
import modulos.recursos.dados_compartilhados as dc

for nome, caminho in dc.imagens_portes.items():
    print(nome, caminho, "->",  os.path.exists(caminho))

import os
import modulos.recursos.dados_compartilhados as dc


from modulos.banco.database import inicializar_banco

if __name__ == "__main__":
    inicializar_banco()


print("Arquivo carregado:", dc.__file__)
print("Portes disponíveis:", getattr(dc, "portes", "NÃO EXISTE"))

caminho_img = os.path.join(dc.BASE_IMAGENS, "rodape", "footer.png")
print("📂 Caminho rodapé:", caminho_img, "->", os.path.exists(caminho_img))



# Caminho base onde estão as imagens das raças
# Caminho base único para todas as imagens
CAMINHO_IMAGENS = "C:/Users/VEIRANO/PycharmProjects/ModuloTkinter/Planilha Controle Ipojucão/imagensipojucao/"


# ✅ Variável global declarada no topo do arquivo
foto_nova_raca = None


def montar_menu_lateral_clientes(container):
    from modulos.componentes.menu_lateral_widget import menu_lateral
    menu_lateral(container)

def inicializar_clientes(scroll_frame):
    # Variáveis compartilhadas
    var_porte = dc.variaveis["var_porte"]
    var_raca = dc.variaveis["var_raca"]

    # -----------------------------
    # Combobox Porte + Imagem
    # -----------------------------
    ttk.Label(scroll_frame, text="Selecione PORTE:").grid(row=1, column=0, sticky="e")
    combo_porte = ttk.Combobox(scroll_frame, textvariable=var_porte, values=list(dc.imagens_portes.keys()), state="readonly")
    combo_porte.grid(row=1, column=1, padx=5, pady=5)
    combo_porte.set("pequeno")  # valor inicial


    label_imagem_porte = ttk.Label(scroll_frame)
    label_imagem_porte.grid(row=1, column=2, padx=10, pady=10)

    def atualizar_imagem_porte(event=None):
        porte = var_porte.get().strip().lower()  # normaliza
        print("👉 Valor selecionado:", porte)
        print("👉 Chaves disponíveis:", list(dc.imagens_portes.keys()))

        for chave in dc.imagens_portes.keys():
            if chave.lower() == porte:
                caminho = dc.imagens_portes[chave]
                print("📂 Caminho da foto porte:", caminho, "->", os.path.exists(caminho))
                try:
                    img = Image.open(caminho).resize((120, 120))
                    foto = ImageTk.PhotoImage(img)
                    label_imagem_porte.config(image=foto)
                    label_imagem_porte.image = foto
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível carregar imagem: {e}")
                break
    # ✅ Chama a função depois de definida
    atualizar_imagem_porte()



    # Label e combobox de raça
    ttk.Label(scroll_frame, text="Selecione RAÇA:").grid(row=1, column=3, sticky="e")
    combo_raca = ttk.Combobox(scroll_frame, textvariable=var_raca, state="readonly")
    combo_raca.grid(row=1, column=4, padx=5, pady=5)


    # Entry escondido para raça nova
    label_imagem_raca = ttk.Label(scroll_frame)
    label_imagem_raca.grid(row=1, column=5, padx=10, pady=10)

    def atualizar_imagem_raca(event=None):
        raca = var_raca.get().strip()
        print("👉 Raça selecionada:", raca)
        print("👉 Chaves disponíveis em imagens_racas:", list(dc.imagens_racas.keys()))

        if raca in dc.imagens_racas:
            caminho = dc.imagens_racas[raca]
            print("📂 Caminho da foto raça:", caminho, "->", os.path.exists(caminho))
            try:
                img = Image.open(caminho).resize((120, 120))
                foto = ImageTk.PhotoImage(img)
                label_imagem_raca.config(image=foto)
                label_imagem_raca.image = foto
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar imagem da raça: {e}")

    # Entry escondido para raça nova
    label_outro = ttk.Label(scroll_frame, text="Digite a raça:")
    entry_outro = ttk.Entry(scroll_frame)




    def escolher_foto():
        global foto_nova_raca
        caminho = filedialog.askopenfilename(
            title="Selecione a foto da raça",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")]
        )
        if caminho:
            foto_nova_raca = caminho
            print(f"📂 Foto selecionada: {foto_nova_raca}")

    btn_foto = ttk.Button(scroll_frame, text="Selecionar Foto", command=escolher_foto)
    btn_foto.grid(row=2, column=6, padx=5)
    btn_foto.grid_remove()

    def salvar_nova_raca():
        global foto_nova_raca
        nova_raca = entry_outro.get().strip()
        porte = var_porte.get()

        if nova_raca and porte in dc.dados_pet:
            # Adiciona a nova raça ao dicionário
            if nova_raca not in dc.dados_pet[porte]["raças"]:
                dc.dados_pet[porte]["raças"].append(nova_raca)

            # Adiciona imagem associada
            if foto_nova_raca:
                dc.imagens_racas[nova_raca] = foto_nova_raca

            # Atualiza combobox
            racas_ordenadas = sorted(dc.dados_pet[porte]["raças"], key=lambda x: x.lower())
            racas_ordenadas.append("Outro")
            combo_raca["values"] = racas_ordenadas
            combo_raca.set(nova_raca)

            # Oculta novamente
            label_outro.grid_remove()
            entry_outro.grid_remove()
            btn_salvar.grid_remove()
            btn_foto.grid_remove()

            print(f"✅ Nova raça adicionada: {nova_raca} com foto {foto_nova_raca}")

            # Salva no JSON
            caminho_json = os.path.join(os.path.dirname(__file__), "..", "racas.json")
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(dc.dados_pet, f, ensure_ascii=False, indent=4)

            caminho_json_img = os.path.join(os.path.dirname(__file__), "..", "imagens_racas.json")
            with open(caminho_json_img, "w", encoding="utf-8") as f:
                json.dump(dc.imagens_racas, f, ensure_ascii=False, indent=4)

            foto_nova_raca = None  # reseta variável

    btn_salvar = ttk.Button(scroll_frame, text="Salvar Raça", command=salvar_nova_raca)
    btn_salvar.grid(row=2, column=5, padx=5)
    btn_salvar.grid_remove()

    def mostrar_entry_outro(event=None):
        if var_raca.get() == "Outro":
            label_outro.grid()
            entry_outro.grid()
            btn_salvar.grid()
            btn_foto.grid()
        else:
            label_outro.grid_remove()
            entry_outro.grid_remove()
            btn_salvar.grid_remove()
            btn_foto.grid_remove()

    # Evento para atualizar imagem da raça
    combo_raca.bind("<<ComboboxSelected>>", atualizar_imagem_raca)

    # Inicializa escondido
    label_outro.grid(row=2, column=3, sticky="e", padx=5)
    entry_outro.grid(row=2, column=4, padx=5)
    label_outro.grid_remove()
    entry_outro.grid_remove()

    # ✅ Bind para mostrar campo e botões quando selecionar "Outro"
    combo_raca.bind("<<ComboboxSelected>>", mostrar_entry_outro)

    def atualizar_racas(event=None):
        porte = var_porte.get()
        if porte in dc.dados_pet:
            racas = dc.dados_pet[porte]["raças"]
            racas_ordenadas = sorted(racas, key=lambda x: x.lower())
            racas_ordenadas.append("Outro")
            combo_raca["values"] = racas_ordenadas
            combo_raca.set("")

    def mostrar_entry_outro(event=None):
        if var_raca.get() == "Outro":
            label_outro.grid()
            entry_outro.grid()
            btn_salvar.grid()
        else:
            label_outro.grid_remove()
            entry_outro.grid_remove()
            btn_salvar.grid_remove()

    # Eventos
    combo_raca.bind("<<ComboboxSelected>>", mostrar_entry_outro)
    combo_porte.bind("<<ComboboxSelected>>", atualizar_racas)
    # mapa_equivalencias = {
    #     "Pastor Alemao": "Pastor Alemão",
    #     "Chow-chow": "Chow Chow",
    #     "Chip-dog": "Chip Dog",
    #     "American Pit Bul terrier": "American Pit Bull Terrier"
    # }

    def atualizar_imagem_raca(event=None):
        raca = var_raca.get()
        print("👉 Raça selecionada:", raca)
        print("👉 Chaves disponíveis em imagens_racas:", list(dc.imagens_racas.keys()))
        if raca in dc.imagens_racas:
            caminho = dc.imagens_racas[raca]
            print("📂 Caminho da foto raça:", caminho, "->", os.path.exists(caminho))
            try:
                img = Image.open(caminho).resize((120, 120))
                foto = ImageTk.PhotoImage(img)
                label_imagem_raca.config(image=foto)
                label_imagem_raca.image = foto
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar imagem: {e}")

    def on_raca_selected(event=None):
        mostrar_entry_outro()
        atualizar_imagem_raca()

    combo_raca.bind("<<ComboboxSelected>>", on_raca_selected)

    def on_porte_selected(event=None):
        atualizar_imagem_porte()
        atualizar_racas()

    combo_porte.bind("<<ComboboxSelected>>", on_porte_selected)


def verificar_conexao():
    testar_conexao()
    if conexao_valida():
        print("✅ Conexão OK")
    else:
        print("❌ Erro na conexão")

verificar_conexao()

def criar_aba_clientes(notebook):
    scroll_frame = ttk.Frame(notebook)

#logo_splash = caminho_arquivo("splash.png", subpasta=os.path.join(dc.BASE_IMAGENS.join("..", "..", "imagensipojucao"))
logo_splash = caminho_arquivo(
    "splash.png",
    subpasta=os.path.join(dc.BASE_IMAGENS, "imagensipojucao")
)
som_relatorio = caminho_arquivo("relatorio_finalizado.mp3", subpasta="sons")

def montar_aba_clientes(master):
    aba_clientes = ttk.Frame(master)
    master.add(aba_clientes, text="Clientes")

    # Canvas + Scrollbar com grid
    canvas = tk.Canvas(aba_clientes, bg="white")
    scrollbar_y = ttk.Scrollbar(aba_clientes, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(aba_clientes, orient="horizontal", command=canvas.xview)

    scroll_frame = ttk.Frame(canvas)
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    aba_clientes.grid_rowconfigure(0, weight=1)
    aba_clientes.grid_columnconfigure(0, weight=1)

    ttk.Label(scroll_frame, text="Cadastro de Clientes", font=("Segoe UI", 20, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(10, 5), sticky="w"
    )

    inicializar_clientes(scroll_frame)

    # Variáveis
    var_porte = dc.variaveis["var_porte"]
    var_raca = dc.variaveis["var_raca"]

    var_porte = dc.variaveis["var_porte"]
    var_raca = dc.variaveis["var_raca"]

    # Variáveis Cliente
    var_id = tk.StringVar()
    var_nome = tk.StringVar()
    var_telefone = tk.StringVar()
    var_email = tk.StringVar()
    var_pet_nome = tk.StringVar()
    var_endereco = tk.StringVar()
    var_numero = tk.StringVar()
    var_complemento = tk.StringVar()
    var_bairro = tk.StringVar()
    var_referencia = tk.StringVar()
    var_cpf = tk.StringVar()
    var_foto_cliente = tk.StringVar()

    # Variáveis Pet
    var_pet_nome = tk.StringVar()
    var_pet_idade_anos = tk.StringVar()
    var_pet_idade_meses = tk.StringVar()
    var_pet_raca = tk.StringVar()
    var_pet_porte = tk.StringVar()
    var_pet_pelagem = tk.StringVar()
    var_pet_caracteristicas = tk.StringVar()
    var_foto_pet = tk.StringVar()

    # 1. Variáveis de busca
    var_busca_nome = tk.StringVar()
    var_busca_id = tk.StringVar()
    var_busca_nome_pet = tk.StringVar()
    var_busca_cpf = tk.StringVar()
    var_busca_email = tk.StringVar()
    var_busca_telefone = tk.StringVar()
    var_busca_endereco = tk.StringVar()
    var_busca_numero = tk.StringVar()
    var_busca_complemento = tk.StringVar()
    var_busca_bairro = tk.StringVar()
    var_busca_ponto_referencia = tk.StringVar()
    var_busca_raca = tk.StringVar()
    var_busca_porte = tk.StringVar()
    var_busca_pet = tk.StringVar()
    var_busca_cliente = tk.StringVar()

    dc.variaveis["var_porte"].get()
    dc.variaveis["var_raca"].get()

    criterio_busca = tk.StringVar()

    # 2. Combobox de critério
    ttk.Label(scroll_frame, text="Critério de Busca:").grid(row=3, column=0, sticky="w", padx=5, pady=5)

    combo_busca = ttk.Combobox(
        scroll_frame,
        textvariable=criterio_busca,
        values=["ID", "Nome Cliente", "Telefone", "Email", "Endereço", "Número", "Bairro", "Ponto de Referência", "CPF", "Nome Pet", "Raça", "Porte"],
        state="readonly",
        width=20
    )
    combo_busca.grid(row=4, column=0, padx=5, pady=5)
    combo_busca.current(1)  # valor padrão: Nome Cliente

    # 3. Campo de texto para valor da busca
    valor_busca = tk.StringVar()
    entry_busca = ttk.Entry(scroll_frame, textvariable=valor_busca, width=30)
    entry_busca.grid(row=4, column=1, padx=5, pady=5)

    def buscar_cliente():
        campo = criterio_busca.get()
        valor = valor_busca.get().strip()

        if not campo or not valor:
            messagebox.showwarning("Aviso", "Selecione um critério e informe um valor para busca.")
            return

        query = session.query(Cliente).join(Pets, isouter=True)

        if campo == "ID":
            query = query.filter(Cliente.id == valor)
        elif campo == "Nome Cliente":
            query = query.filter(Cliente.nome.ilike(f"%{valor}%"))
        elif campo == "Telefone":
            query = query.filter(Cliente.telefone.ilike(f"%{valor}%"))
        elif campo == "Email":
            query = query.filter(Cliente.email.ilike(f"%{valor}%"))
        elif campo == "Endereço":
            query = query.filter(Cliente.endereco.ilike(f"%{valor}%"))
        elif campo == "Número":
            query = query.filter(Cliente.numero.ilike(f"%{valor}%"))
        elif campo == "Bairro":
            query = query.filter(Cliente.bairro.ilike(f"%{valor}%"))
        elif campo == "Ponto de Referência":
            query = query.filter(Cliente.ponto_referencia.ilike(f"%{valor}%"))
        elif campo == "CPF":
            query = query.filter(Cliente.cpf.ilike(f"%{valor}%"))
        elif campo == "Nome Pet":
            query = query.filter(Pets.nome.ilike(f"%{valor}%"))
        elif campo == "Raça":
            query = query.filter(Pets.raca.ilike(f"%{valor}%"))
        elif campo == "Porte":
            query = query.filter(Pets.porte.ilike(f"%{valor}%"))

        resultados = query.all()

        # Limpar Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Inserir resultados
        for cliente in resultados:
            tree.insert("", "end", values=(
                cliente.id,
                cliente.nome,
                cliente.telefone,
                cliente.email,
                cliente.cpf,
                cliente.endereco,
                cliente.numero,
                cliente.complemento,
                cliente.bairro,
                cliente.ponto_referencia
            ))

    # 4. Botão de busca
    btn_buscar = ttk.Button(scroll_frame, text="🔍 Buscar", command=lambda: buscar_cliente())
    btn_buscar.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")

    ttk.Label(scroll_frame, text="Dados do Clientes", font=("Segoe UI", 14, "bold")).grid(
        row=5, column=1, pady=(10, 5), sticky="w"
    )

    ttk.Label(scroll_frame, text="id:").grid(row=6, column=1, sticky="e")
    entry_id = ttk.Entry(scroll_frame, textvariable=var_busca_id, width=30)
    entry_id.grid(row=6, column=2)

    ttk.Label(scroll_frame, text="Nome Cliente:").grid(row=6, column=2, sticky="e")
    entry_nome = ttk.Entry(scroll_frame, textvariable=var_busca_nome, width=30)
    entry_nome.grid(row=6, column=3)

    ttk.Label(scroll_frame, text="Telefone:").grid(row=7, column=1, sticky="e")
    entry_telefone = ttk.Entry(scroll_frame, textvariable=var_busca_telefone, width=30)
    entry_telefone.grid(row=7, column=2)

    ttk.Label(scroll_frame, text="Email:").grid(row=7, column=3, sticky="e")
    entry_email = ttk.Entry(scroll_frame, textvariable=var_busca_email, width=30)
    entry_email.grid(row=7, column=4)

    ttk.Label(scroll_frame, text="Endereço:").grid(row=8, column=1, sticky="e")
    entry_endereco = ttk.Entry(scroll_frame, textvariable=var_busca_endereco, width=30)
    entry_endereco.grid(row=8, column=2, columnspan=3, sticky="nsew")

    ttk.Label(scroll_frame, text="Número:").grid(row=8, column=3, sticky="e")
    entry_numero = ttk.Entry(scroll_frame, textvariable=var_busca_numero, width=30)
    entry_numero.grid(row=8, column=4)

    ttk.Label(scroll_frame, text="Complemento:").grid(row=9, column=1, sticky="e")
    entry_complemento = ttk.Entry(scroll_frame, textvariable=var_busca_complemento, width=30)
    entry_complemento.grid(row=9, column=2)

    ttk.Label(scroll_frame, text="Bairro:").grid(row=9, column=3, sticky="e")
    entry_bairro = ttk.Entry(scroll_frame, textvariable=var_busca_bairro, width=30)
    entry_bairro.grid(row=9, column=4)

    ttk.Label(scroll_frame, text="Ponto de Referência:").grid(row=10, column=1, sticky="e")
    entry_referencia = ttk.Entry(scroll_frame, textvariable=var_busca_ponto_referencia, width=30)
    entry_referencia.grid(row=10, column=2)

    # ttk.Label(scroll_frame, text="Raça:").grid(row=6, column=4, sticky="w")
    # entry_raca = ttk.Entry(scroll_frame, textvariable=var_busca_raca, width=30)
    # entry_raca.grid(row=6, column=5)
    #
    # ttk.Label(scroll_frame, text="Porte:").grid(row=6, column=6, sticky="w")
    # entry_porte = ttk.Entry(scroll_frame, textvariable=var_busca_porte, width=30)
    # entry_porte.grid(row=6, column=7)




    ttk.Label(scroll_frame, text="Dados do PET", font=("Segoe UI", 14, "bold")).grid(
        row=12, column=1, columnspan=2, pady=(10, 5), sticky="w"
    )

    # Campos Pet
    ttk.Label(scroll_frame, text="Nome do Pet:").grid(row=14, column=1, sticky="e")
    entry_pet_nome = ttk.Entry(scroll_frame, textvariable=var_pet_nome, width=40)
    entry_pet_nome.grid(row=14, column=2, sticky="e")


    var_porte = tk.StringVar()
    var_raca = tk.StringVar()

    ttk.Label(scroll_frame, text="Idade (anos):").grid(row=14, column=3, sticky="e")
    entry_pet_idade_anos = ttk.Entry(scroll_frame, textvariable=var_pet_idade_anos, width=10)
    entry_pet_idade_anos.grid(row=14, column=4, sticky="e")

    ttk.Label(scroll_frame, text="Idade (meses):").grid(row=14, column=5, sticky="e")
    entry_pet_idade_meses = ttk.Entry(scroll_frame, textvariable=var_pet_idade_meses, width=10)
    entry_pet_idade_meses.grid(row=14, column=6, sticky="e")

    ttk.Label(scroll_frame, text="Pelagem:").grid(row=15, column=1, sticky="e")
    entry_pet_pelagem = ttk.Entry(scroll_frame, textvariable=var_pet_pelagem, width=40)
    entry_pet_pelagem.grid(row=15, column=2, sticky="e")

    ttk.Label(scroll_frame, text="Características:").grid(row=16, column=1, sticky="e")
    entry_pet_caracteristicas = ttk.Entry(scroll_frame, textvariable=var_pet_caracteristicas, width=40)
    entry_pet_caracteristicas.grid(row=16, column=2, sticky="e")

    ttk.Label(scroll_frame, text="Informações Importantes Sobre o PET", font=("Segoe UI", 14, "bold")).grid(
        row=19, column=3, pady=(10, 5), sticky="e"
    )

    def salvar_cliente():
        with SessionLocal() as session:
            cliente = Cliente(
                nome=entry_nome.get(),
                telefone=entry_telefone.get(),
                email=entry_email.get(),
                endereco=entry_endereco.get(),
                numero=entry_numero.get(),
                complemento=entry_complemento.get(),
                bairro=entry_bairro.get(),
                referencia=entry_referencia.get()
            )

            # exemplo de 1 PET
            pet1 = Pet(
                nome=entry_pet_nome.get(),
                raca=entry_pet_raca.get(),
                idade_anos=int(entry_pet_idade_anos.get()),
                idade_meses=int(entry_pet_idade_meses.get()),
                pelagem=entry_pet_pelagem.get(),
                caracteristicas=entry_pet_caracteristicas.get(),
                foto_principal=foto_pet.get()
            )

            cliente.pets.append(pet1)
            session.add(cliente)
            session.commit()

    # buttons (BooleanVar)
    # Variáveis
    var_problemas_pele = tk.BooleanVar()
    var_problemas_saude = tk.BooleanVar()
    var_shampoo_terapeutico = tk.BooleanVar()
    var_hidratante_terapeutico = tk.BooleanVar()
    var_outras_info = tk.BooleanVar()

    var_descricao_saude = tk.StringVar()
    var_descricao_outras_info = tk.StringVar()

    # Checkbuttons
    chk_pele = ttk.Checkbutton(scroll_frame, text="Problemas de Pele", variable=var_problemas_pele)
    chk_pele.grid(row=21, column=0, sticky="w", pady=2)

    chk_shampoo = ttk.Checkbutton(scroll_frame, text="Usa Shampoo Terapêutico", variable=var_shampoo_terapeutico)
    chk_shampoo.grid(row=22, column=0, sticky="w", pady=2)

    chk_hidratante = ttk.Checkbutton(scroll_frame, text="Usa Hidratante Terapêutico", variable=var_hidratante_terapeutico)
    chk_hidratante.grid(row=23, column=0, sticky="w", pady=2)

    chk_saude = ttk.Checkbutton(scroll_frame, text="Problemas de Saúde", variable=var_problemas_saude,
                                command=lambda: toggle_saude())
    chk_saude.grid(row=21, column=1, sticky="w", pady=2)

    chk_outras = ttk.Checkbutton(scroll_frame, text="Outras Informações Importantes", variable=var_outras_info,
                                 command=lambda: toggle_outras())
    chk_outras.grid(row=22, column=1, sticky="w", pady=2)

    # Campos condicionais (inicialmente ocultos)
    txt_saude = tk.Entry(scroll_frame, textvariable=var_descricao_saude)
    txt_outras = tk.Entry(scroll_frame, textvariable=var_descricao_outras_info)

    # Funções para mostrar/ocultar
    def toggle_saude():
        if var_problemas_saude.get():
            txt_saude.grid(row=21, column=2, padx=5, pady=2)
        else:
            txt_saude.grid_remove()

    def toggle_outras():
        if var_outras_info.get():
            txt_outras.grid(row=22, column=2, padx=5, pady=2)
        else:
            txt_outras.grid_remove()

    # Variáveis para os Radiobuttons
    var_secador = tk.StringVar(value="não")
    var_soprador = tk.StringVar(value="não")
    var_perfume = tk.StringVar(value="não")
    var_aderecos = tk.StringVar(value="não")

    # Radiobuttons ao lado direito
    # Secador
    ttk.Label(scroll_frame, text="Secador:").grid(row=21, column=3, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Sim", variable=var_secador, value="sim").grid(row=21, column=4, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Não", variable=var_secador, value="não").grid(row=21, column=5, sticky="w")

    # Soprador
    ttk.Label(scroll_frame, text="Soprador:").grid(row=22, column=3, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Sim", variable=var_soprador, value="sim").grid(row=22, column=4, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Não", variable=var_soprador, value="não").grid(row=22, column=5, sticky="w")

    # Perfume
    ttk.Label(scroll_frame, text="Perfume:").grid(row=23, column=3, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Sim", variable=var_perfume, value="sim").grid(row=23, column=4, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Não", variable=var_perfume, value="não").grid(row=23, column=5, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Pouco", variable=var_perfume, value="pouco").grid(row=23, column=6, sticky="w")

    # Adereços
    ttk.Label(scroll_frame, text="Adereços:").grid(row=24, column=3, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Sim", variable=var_aderecos, value="sim").grid(row=24, column=4, sticky="w")
    ttk.Radiobutton(scroll_frame, text="Não", variable=var_aderecos, value="não").grid(row=24, column=5, sticky="w")

    # FOTO CLIENTE

    def selecionar_foto_cliente():
        caminho = filedialog.askopenfilename(
            title="Selecione a foto do Cliente",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")]
        )
        if caminho:
            var_foto_cliente.set(caminho)
            mostrar_foto_cliente(caminho)

    def mostrar_foto_cliente(caminho):
        img = Image.open(caminho)
        img = img.resize((120, 120))  # redimensiona
        foto = ImageTk.PhotoImage(img)
        lbl_foto_cliente.config(image=foto)
        lbl_foto_cliente.image = foto  # mantém referência

    # Botão e Label
    btn_foto_cliente = ttk.Button(scroll_frame, text="Selecionar Foto Cliente", command=selecionar_foto_cliente)
    btn_foto_cliente.grid(row=6, column=0, padx=5, pady=5)

    lbl_foto_cliente = ttk.Label(scroll_frame)
    lbl_foto_cliente.grid(row=7, column=0, padx=5, pady=5)

    # FOTO PET

    def selecionar_foto_pet():
        caminho = filedialog.askopenfilename(
            title="Selecione a foto do Pet",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")]
        )

        if caminho:
            var_foto_pet.set(caminho)
            mostrar_foto_pet(caminho)

    def mostrar_foto_pet(caminho):
        img = Image.open(caminho)
        img = img.resize((120, 120))
        foto = ImageTk.PhotoImage(img)
        lbl_foto_pet.config(image=foto)
        lbl_foto_pet.image = foto

    btn_foto_pet = ttk.Button(scroll_frame, text="Selecionar Foto Pet", command=selecionar_foto_pet)
    btn_foto_pet.grid(row=14, column=0, padx=5, pady=5)

    lbl_foto_pet = ttk.Label(scroll_frame)
    lbl_foto_pet.grid(row=15, column=0 , padx=5, pady = 5)

    # Treeview
    cols = (
    "ID", "Nome", "Telefone", "Email", "Endereço", "Número", "Complemento", "Bairro", "Ponto de Referência", "CPF")
    tree = ttk.Treeview(scroll_frame, columns=cols, show="headings", height=8)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")  # largura fixa



    # tree = ttk.Treeview(
    #     scroll_frame,
    #     columns=(
    #     "ID", "Nome", "Telefone", "Email", "Endereço", "Número", "Complemento", "Bairro", "Ponto de Referência", "CPF"),
    #     show="headings"
    # )

    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Email", text="Email")
    tree.heading("Endereço", text="Endereço")
    tree.heading("Número", text="Número")
    tree.heading("Complemento", text="Complemento")
    tree.heading("Bairro", text="Bairro")
    tree.heading("Ponto de Referência", text="Ponto de Referência")   # ✅ corrigido
    tree.heading("CPF", text="CPF")


    for i in range(20):  # colunas 0 até 9
        scroll_frame.grid_columnconfigure(i, weight=1)
    scroll_frame.grid_rowconfigure(10, weight=1)
    # Scrollbars
    scroll_y = ttk.Scrollbar(scroll_frame, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(scroll_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tree.grid(row=34, column=0, columnspan=12, padx=5, pady=5, sticky="nsew")
    scroll_y.grid(row=34, column=12, sticky="nsew")
    scroll_x.grid(row=35, column=0, columnspan=20, sticky="nsew")

    # ✅ Aqui entram os comandos de expansão
    for i in range(20):  # número máximo de colunas que você usa
        scroll_frame.grid_columnconfigure(i, weight=1)

    for j in range(40):  # número máximo de linhas que você usa
        scroll_frame.grid_rowconfigure(j, weight=1)

    # Funções internas
    def salvar_pet():
        porte = var_porte.get()
        raca_selecionada = var_raca.get()

        if raca_selecionada == "Outro":
            raca_final = entry_raca_outro.get().strip()
            # ✅ adiciona automaticamente ao dicionário
            if raca_final and raca_final not in dc.dados_pet[porte]["raças"]:
                dc.dados_pet[porte]["raças"].append(raca_final)
                dc.dados_pet[porte]["raças"] = sorted(dc.dados_pet[porte]["raças"], key=lambda x: x.lower())
        else:
            raca_final = raca_selecionada.get()

            # aqui você cria o objeto Pet normalmente
        pet = Pet(
            nome=entry_pet_nome.get(),
            raca=raca_final,
            idade_anos=int(entry_pet_idade_anos.get() or 0),
            idade_meses=int(entry_pet_idade_meses.get() or 0),
            pelagem=entry_pet_pelagem.get(),
            caracteristicas=entry_pet_caracteristicas.get(),
            foto_principal=entry_pet_foto.get()
        )
        cliente.pets.append(pet)

        if not var_id.get():
            messagebox.showwarning("Aviso", "Cadastre ou selecione um cliente primeiro.")
            return
        pet = Pets(nome=var_pet_nome.get().strip(), cliente_id=int(var_id.get()))
        database.session.add(pet)
        database.session.commit()
        messagebox.showinfo("Sucesso", f"Pet {pet.nome} cadastrado para cliente {var_nome.get()}")
        var_pet_nome.set("")

    def carregar_clientes():
        tree.delete(*tree.get_children())
        clientes = session.query(Cliente).all()
        for c in clientes:
            tree.insert("", "end", values=(c.id, c.nome, c.telefone, c.email, c.cpf))

    def salvar_cliente():
        try:
            novo_cliente = Cliente(
                nome=var_nome.get().strip(),
                telefone=var_telefone.get().strip(),
                email=var_email.get().strip(),
                cpf=var_cpf.get().strip(),
                raca=var_pet_raca.get().strip(),
                porte=var_pet_porte.get().strip(),
                descricao_pelagem=var_pet_pelagem.get().strip(),
                foto=var_foto_pet.get().strip(),
                problemas_pele=var_problemas_pele.get(),
                problemas_saude=var_problemas_saude.get(),
                descricao_saude=var_descricao_saude.get().strip() if var_problemas_saude.get() else None,
                shampoo_terapeutico=var_shampoo_terapeutico.get(),
                hidratante_terapeutico=var_hidratante_terapeutico.get(),
                outras_info=var_outras_info.get(),
                descricao_outras_info=var_descricao_outras_info.get().strip() if var_outras_info.get() else None
            )

            session.add(novo_cliente)
            session.commit()
            messagebox.showinfo("Sucesso", f"Cliente {novo_cliente.nome} cadastrado com ID {novo_cliente.id}")
            carregar_clientes()
            limpar_campos()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}")

    def excluir_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Selecione", "Escolha um cliente na lista.")
            return
        id_sel = int(tree.item(item[0], "values")[0])
        resultado = excluir_cliente_por_id(id_sel)
        messagebox.showinfo("Resultado", resultado)
        carregar_clientes()
        limpar_campos()

    def editar_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Selecione", "Escolha um cliente na lista.")
            return

        id_sel, nome_sel, telefone_sel, email_sel, endereco_sel, numero_sel, complemento_sel, bairro_sel, referencia_sel, cpf_sel, foto_cliente_sel = tree.item(item[0], "values")
        var_id.set(id_sel)
        var_nome.set(nome_sel)
        var_telefone.set(telefone_sel)
        var_email.set(email_sel)
        var_endereco = tk.StringVar()
        var_numero = tk.StringVar()
        var_complemento = tk.StringVar()
        var_bairro = tk.StringVar()
        var_referencia = tk.StringVar()
        var_cpf = tk.StringVar()
        var_foto_cliente = tk.StringVar()

        # Agora sim, dentro da função
        cliente = session.get(Cliente, id_sel)

        var_endereco.set(cliente.endereco or "")
        var_numero.set(cliente.numero or "")
        var_complemento.set(cliente.complemento or "")
        var_bairro.set(cliente.bairro or "")
        var_referencia.set(cliente.ponto_referencia or "")
        var_foto_cliente.set(cliente.foto_cliente or "")

        # Se tiver pet vinculado
        pet = session.query(Pets).filter_by(tutor_id=cliente.id).first()
        if pet:
            var_pet_nome.set(pet.nome or "")
            var_pet_raca.set(pet.raca or "")
            var_pet_porte.set(pet.porte or "")
            var_pet_pelagem.set(pet.descricao_pelagem or "")
            var_pet_caracteristicas.set(pet.caracteristicas or "")
            var_foto_pet.set(pet.foto or "")

        # buttons
        var_problemas_pele.set(pet.problemas_pele)
        var_problemas_saude.set(pet.problemas_saude)
        var_descricao_saude.set(pet.descricao_saude or "")
        var_shampoo_terapeutico.set(pet.shampoo_terapeutico)
        var_hidratante_terapeutico.set(pet.hidratante_terapeutico)
        var_outras_info.set(pet.outras_info)
        var_descricao_outras_info.set(pet.descricao_outras_info or "")

    def buscar_clientes():
        termo = var_nome.get().strip()
        tree.delete(*tree.get_children())
        resultados = buscar_clientes_por_nome(termo)
        for r in resultados:
            tree.insert("", "end", values=(r.id, r.nome, r.telefone, r.email, r.cpf))
            messagebox.showinfo("Busca concluída", f"Foram encontrados {len(resultados)} clientes")

    def limpar_campos():
        var_id.set("")
        var_nome.set("")
        var_telefone.set("")
        var_email.set("")
        var_cpf.set("")

    # Botões
    ttk.Button(scroll_frame, text="Salvar", command=salvar_cliente).grid(row=26, column=0, sticky="w", pady=5)
    ttk.Button(scroll_frame, text="Buscar por Nome", command=buscar_clientes).grid(row=26, column=1, sticky="w", pady=5)
    ttk.Button(scroll_frame, text="Editar Selecionado", command=editar_cliente).grid(row=26, column=2, sticky="w", pady=5)
    ttk.Button(scroll_frame, text="🗑 Excluir Selecionado", command=excluir_cliente).grid(row=27, column=0, sticky="w", pady=5)
    ttk.Button(scroll_frame, text="🧹 Limpar Campos", command=limpar_campos).grid(row=27, column=1, sticky="w", pady=5)
    ttk.Button(scroll_frame, text="Adicionar Pet", command=salvar_pet).grid(row=27, column=2, sticky="w", pady=5)

    carregar_clientes()

    #return scroll_frame

    return aba_clientes   # ✅ importante


def trocar_aba(self, nome, notebook):
    if nome in self.abas:
        conteudo = self.abas[nome](notebook)  # chama função registrada
        notebook.add(conteudo, text=nome.capitalize())
        notebook.select(notebook.index("end") - 1)
        return conteudo
    else:
        print(f"Aba {nome} não encontrada")
        return None

# def rodape_imagem(scroll_frame_pai):
#     caminho_img = os.path.join(dc.BASE_IMAGENS.join("imagensipojucao", "rodape", "footer.png")
#     if : os.path.join(dc.BASE_IMAGENS,.exists(caminho_img):
#         img = Image.open(caminho_img).resize((1000, 80))
#         img_tk = ImageTk.PhotoImage(img)
#         rodape = tk.Label(scroll_frame_pai, image=img_tk)
#         rodape.image = img_tk  # mantém referência da imagem
#
#         # Posiciona no final da grid
#         rodape.grid(row=50, column=0, columnspan=5, sticky="nsew")  # usa row "alta" para evitar conflito
#     else:
#         print("Imagem do rodapé não encontrada.")

def rodape_imagem(scroll_frame_pai):
    # monta o caminho absoluto para a imagem do rodapé
    caminho_img = os.path.join(dc.BASE_IMAGENS, "rodape", "footer.png")

    if os.path.exists(caminho_img):
        try:
            img = Image.open(caminho_img).resize((1000, 80))
            img_tk = ImageTk.PhotoImage(img)

            rodape = tk.Label(scroll_frame_pai, image=img_tk)
            rodape.image = img_tk  # mantém referência para não perder a imagem

            # posiciona no final da grid
            rodape.grid(row=50, column=0, columnspan=5, sticky="nsew")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar rodapé: {e}")
    else:
        print(f"⚠️ Imagem do rodapé não encontrada: {caminho_img}")


if __name__ == "__main__":
    #enviar_mensagem_whatsapp("+5511999999999", "Olá, Reinaldo! Teste de envio via Python.")

#enviar_mensagem_whatsapp("+5511999999999", "Olá, Reinaldo! Teste de envio via Python.")


    tocar_som("sons/usuario_adicionado.mp3")

