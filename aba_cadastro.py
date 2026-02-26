#from recursos.dados_compartilhados import (var_porte, var_raca)

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from modulos.componentes.mascote_widget import criar_aba_mascote_widget, mostrar_mascote_expressivo
from modulos.recursos.utils_imagem import carregar_imagem_tk
from tkinter import Label

from recursos.dados_compartilhados import som_global_ativo
from recursos.som import som_evento

janela = tk.Tk()
label = tk.Label(janela)
label.grid(row=0, column=0, padx=10, pady=10)

label = Label(janela)  # ou frame, ou outro container
label.grid(row=0, column=0, padx=10, pady=10)


# img = carregar_imagem_tk("logo_ipojucao.png")
# label.config(image=img)
# label.img_ref = img  # manter referência


# from modulos.abas.aba_som_legacy import som_cadastro
from modulos.recursos.som import inicializar_audio, ativar_som, desativar_som, alternar_som, som_ativo, tocar_som,tocar_som_curto, parar_som, som_evento
som_evento, som_ativo, som_global_ativo# ✅ novo
# ABA CADASTRO REFORMULADA, PARTE 1

import os
# Imports locais e compartilhados
from modulos.recursos.dados_compartilhados import (caracteristicas_racas, imagens_portes, imagens_racas, )
from modulos.recursos import dados_compartilhados as dc
#from modulos.abas.mascote import mostrar_mascote_expressivo
from recursos.utilitarios import caminho_arquivo

# ===============================
# Importações Após Reestruturação do Projeto (abaixo)
import recursos.dados_compartilhados as dc
from modulos.banco.database import testar_conexao

from recursos.conexao_utils import conexao_valida
from modulos.componentes.menu_lateral_widget import menu_lateral

# from modulos.abas.mensageiro import enviar_mensagem_whatsapp
#
# enviar_mensagem_whatsapp("+5511999999999", "Olá, Reinaldo! Teste de envio via Python.")


def verificar_conexao():
    testar_conexao()
    if conexao_valida():
        print("✅ Conexão OK")
    else:
        print("❌ Erro na conexão")

verificar_conexao()
# Importações Após Reestruturação do Projeto (acima)
# ===============================


# . Importações específicas por aba ( aba_cadastro, aba_clientes, aba_consulta) - abaixo

# . Importações específicas por aba ( aba_cadastro, aba_clientes, aba_consulta) - acima


def inicializar_cadastro(master):
    dc.inicializar_variaveis(master)






#importações para menú em tela boas vindas e chamada das abas
# Importa funções de montagem das abas

# Importa o inner_frame compartilhado
from recursos.estrutura import inner_frame
#importações para menú em tela boas vindas e chamada de abas


logo_splash = caminho_arquivo("splash.png", subpasta=os.path.join("../..", "..", "imagensipojucao"))
som_relatorio = caminho_arquivo("relatorio_finalizado.mp3", subpasta="sons")

# from dados_compartilhados import(
#     var_porte, var_raca, var_tipopelo, var_descricao,
#     caracteristicas_racas, imagens_portes, imagens_racas
# )

    # Botão imagem do PET
    # btn_img_pet = ttk.Button(frame_pet, text="📷 Adicionar imagem do PET", command=lambda: selecionar_imagem_pet(frame_pet))
    # btn_img_pet.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # 👥 Dados dos tutores
def montar_aba_cadastro(frame_pai, inner_frame):
    # aqui vai o frame_tutor e os widgets
    frame_tutor = ttk.LabelFrame(inner_frame, text="👥 Dados dos Tutores", padding=10)
    frame_tutor.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    tk.Label(frame_tutor, text="Tutor 1:").grid(row=0, column=0, sticky="w", padx=5)
    entry_tutor1 = tk.Entry(frame_tutor)
    entry_tutor1.grid(row=0, column=1, padx=5)

    tk.Label(frame_tutor, text="Telefone:").grid(row=1, column=0, sticky="w", padx=5)
    entry_tel1 = tk.Entry(frame_tutor)
    entry_tel1.grid(row=1, column=1, padx=5)

    tk.Label(frame_tutor, text="Email:").grid(row=2, column=0, sticky="w", padx=5)
    entry_email1 = tk.Entry(frame_tutor)
    entry_email1.grid(row=2, column=1, padx=5)

    # Botão imagem Tutor 1
    btn_img_tutor1 = ttk.Button(frame_tutor, text="📷 Imagem Tutor 1", command=lambda: selecionar_imagem_tutor(frame_tutor))
    btn_img_tutor1.grid(row=3, column=0, columnspan=2, pady=5)

    # Tutor 2
    tk.Label(frame_tutor, text="Tutor 2:").grid(row=4, column=0, sticky="w", padx=5)
    entry_tutor2 = tk.Entry(frame_tutor)
    entry_tutor2.grid(row=4, column=1, padx=5)

    tk.Label(frame_tutor, text="Telefone:").grid(row=5, column=0, sticky="w", padx=5)
    entry_tel2 = tk.Entry(frame_tutor)
    entry_tel2.grid(row=5, column=1, padx=5)

    tk.Label(frame_tutor, text="Email:").grid(row=6, column=0, sticky="w", padx=5)
    entry_email2 = tk.Entry(frame_tutor)
    entry_email2.grid(row=6, column=1, padx=5)

    # Botão imagem Tutor 2
    btn_img_tutor2 = ttk.Button(frame_tutor, text="📷 Imagem Tutor 2", command=lambda: selecionar_imagem_tutor(frame_tutor))
    btn_img_tutor2.grid(row=7, column=0, columnspan=2, pady=5)



def salvar_imagem_com_id(tipo, id_unico, caminho_imagem):
    """
    tipo: 'pet' ou 'tutor'
    id_unico: identificador numérico ou string do pet/tutor
    caminho_imagem: caminho da imagem selecionada pelo usuário
    """
    # 🔁 Diretórios
    diretorios = {
        "pet": "imagensipojucao/pets",
        "tutor": "imagensipojucao/tutores"
    }

    # 🧭 Destino
    pasta_destino = diretorios.get(tipo)
    if not pasta_destino:
        print("Tipo inválido:", tipo)
        return

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    destino = os.path.join(pasta_destino, f"{tipo}_{id_unico}.jpg")

    # 🖼️ Redimensionamento
    try:
        img = Image.open(caminho_imagem).resize((160, 160))
        img.save(destino)
        print(f"Imagem {tipo} salva em:", destino)
    except Exception as e:
        print("Erro ao salvar imagem:", e)


# ABA CADASTRO REFORMULADA, PARTE 3


    # 🏠 Endereço
    frame_endereco = ttk.LabelFrame(inner_frame, text="📍 Endereço do PET/Tutor", padding=10)
    frame_endereco.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    tk.Label(frame_endereco, text="Logradouro:").grid(row=0, column=0, sticky="w", padx=5)
    entry_logradouro = tk.Entry(frame_endereco, width=40)
    entry_logradouro.grid(row=0, column=1, padx=5)

    tk.Label(frame_endereco, text="Número:").grid(row=1, column=0, sticky="w", padx=5)
    entry_numero = tk.Entry(frame_endereco, width=10)
    entry_numero.grid(row=1, column=1, sticky="w", padx=5)

    tk.Label(frame_endereco, text="Complemento:").grid(row=2, column=0, sticky="w", padx=5)
    entry_complemento = tk.Entry(frame_endereco, width=30)
    entry_complemento.grid(row=2, column=1, padx=5)

    # 📝 Observações
    frame_obs = ttk.LabelFrame(inner_frame, text="📘 Observações sobre o PET", padding=10)
    frame_obs.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    campo_obs = tk.Text(frame_obs, width=80, height=6)
    campo_obs.pack(padx=5, pady=5)


# ACIMA ABA CADASTRO REFORMULADA PARTE 3

#ABAIXO ABA CADASTRO REFORMULADA PARTE 4


    # ⏱️ Tempo de atendimento
    frame_tempo = ttk.LabelFrame(inner_frame, text="⏱️ Tempo de Atendimento", padding=10)
    frame_tempo.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    tempos = [
        ("Banho", "entry_banho"),
        ("Secagem", "entry_secagem"),
        ("Hidratação", "entry_hidratacao"),
        ("Desembolo", "entry_desembolo"),
        ("Tosa Higiênica", "entry_higienica"),
        ("Tosa Máquina", "entry_maquina"),
        ("Tosa Tesoura", "entry_tesoura"),
        ("Total Atendimento", "entry_total")
    ]
    entradas_tempo = {}

    for i, (label, varname) in enumerate(tempos):
        tk.Label(frame_tempo, text=label + ":").grid(row=i, column=0, sticky="w", padx=5)
        entradas_tempo[varname] = tk.Entry(frame_tempo, width=10)
        entradas_tempo[varname].grid(row=i, column=1, padx=5)

    # 💾 Botão Salvar
def salvar_dados_pet():
    dados = {
        "nome": dc.variaveis["var_nome"].get()
,
        "porte": dc.variaveis["var_porte"].get()
,
        "raca": dc.variaveis["var_raca"].get()
,
        "idade_anos": dc.variaveis["var_idade_anos"].get()
,
        "idade_meses": dc.variaveis["var_idade_meses"].get()
,
        "data_cadastro": dc.variaveis["var_data_cadastro"].get()
,
        "tutor1": dc.variaveis["var_tutor1"].get()
,
        "tutor2": dc.variaveis["var_tutor2"].get()
,
        "logradouro": dc.variaveis["var_logradouro"].get()
,
        "numero": dc.variaveis["var_numero"].get()
,
        "complemento": dc.variaveis["var_complemento"].get()
,
        "obs": campo_obs.get("1.0", "end").strip(),
        "tipopelo": dc.variaveis["var_tipopelo"].get()
,
        "pelagem": dc.variaveis["var_pelagem"].get()
,
        "tempos": {et: entradas_tempo[et].get() for et in entradas_tempo}
        }

def salvar_dados_pet():
    dados = {
            "nome": dc.variaveis["var_nome"].get(),
            "porte": dc.variaveis["var_porte"].get(),
            "raca": dc.variaveis["var_raca"].get(),
            "idade_anos": dc.variaveis["var_idade_anos"].get(),
            "idade_meses": dc.variaveis["var_idade_meses"].get(),
            "tipopelo": dc.variaveis["var_tipopelo"].get(),
            "pelagem": dc.variaveis["var_pelagem"].get(),
            "caracteristicas": dc.variaveis["var_caracteristicas"].get(),
            "data_cadastro": dc.variaveis["var_data_cadastro"].get(),

            # Dados dos tutores
            "tutor1": dc.variaveis["var_tutor1"].get(),
            "tel1": dc.variaveis["var_tel1"].get(),
            "email1": dc.variaveis["var_email1"].get(),
            "tutor2": dc.variaveis["var_tutor2"].get(),
            "tel2": dc.variaveis["var_tel2"].get(),
            "email2": dc.variaveis["var_email2"].get(),

            # Endereço
            "logradouro": dc.variaveis["var_logradouro"].get(),
            "numero": dc.variaveis["var_numero"].get(),
            "complemento": dc.variaveis["var_complemento"].get(),

            # Observações
            "obs": campo_obs.get("1.0", "end").strip(),

                # Tempo de atendimento
                "tempos": {et: entradas_tempo[et].get() for et in entradas_tempo}
            }

# Aqui você pode salvar em arquivo, banco de dados, ou apenas imprimir
def salvar_dados_pet():
    print("🐾 Dados do PET cadastrados:")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")




        btn_audio = tk.Button(inner_frame, text="🔊 Áudio")
        btn_audio.grid(row=10, column=0, padx=10, pady=5)

        som_cadastro("salvando.mp3")  # som personalizado
        from aba_som_legacy import alternar_som_estado
        btn_audio.config(command=lambda: alternar_som_estado(btn_audio))

        #     "nome": entry_nome_pet.get(),
        #     "porte": var_porte.get(),
        #     "raca": var_raca.get(),
        #     "idade_anos": entry_idade_anos.get(),
        #     "idade_meses": entry_idade_meses.get(),
        #     "data_cadastro": data_cadastro.get_date(),
        #     "tutor1": entry_tutor1.get(),
        #     "tutor2": entry_tutor2.get(),
        #     "logradouro": entry_logradouro.get(),
        #     "numero": entry_numero.get(),
        #     "complemento": entry_complemento.get(),
        #     "obs": campo_obs.get("1.0", "end").strip(),
        #     "tipopelo": var_tipopelo.get(),
        #     "pelagem": var_descricao.get(),
        #     "tempos": {et: entradas_tempo[et].get() for et in entradas_tempo}
        # }
        print("📦 Dados do PET salvos:", dados)
        tk.messagebox.showinfo("Cadastro", "Dados do PET salvos com sucesso!")

    btn_salvar = ttk.Button(inner_frame, text="💾 Salvar Cadastro", command=salvar_dados_pet)
    btn_salvar.grid(row=10, column=0, columnspan=2, pady=10)


#from main_backup import var_descricao


# (ABAIXO) VERIFICAR SE ESTE CÓDIGO ESTÁ NA ORDEM CORRETA
    # Busca por CPF
def buscar_por_cpf(cpf_digitado):
    for pet in todos_os_pets_cadastrados:
        if pet["cpf_tutor"] == cpf_digitado:
            return pet["id_pet"]
    return None
# (ACIMA)  VERIFICAR SE ESTE CÓDIGO ESTÁ NA ORDEM CORRETA



def montar_aba_cadastro(aba_cadastro, inner_frame):
    ttk.Label(aba_cadastro, text="Descrição:").grid(row=0, column=0, padx=10, pady=10)
    entry_descricao = ttk.Entry(aba_cadastro, textvariable=dc.variaveis["var_descricao"])
    entry_descricao.grid(row=0, column=1, padx=10, pady=10)

    # ✅ Agora é seguro usar o .set() aqui
    #dc.var_descricao.set("texto exemplo")
    dc.variaveis["var_descricao"].set("Branco")


    # Canvas com inner_frame rolável
    canvas = tk.Canvas(aba)
    scrollbar = ttk.Scrollbar(aba, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner_frame.bind("<Configure>", ajustar_scroll)

    # Título
    titulo = tk.Label(inner_frame, text="Cadastro de PETs", font=("Segoe UI", 16))
    titulo.grid(row=0, column=0, columnspan=2, pady=10)

    # Combobox Porte
    ttk.Label(inner_frame, text="Porte:").grid(row=1, column=0, sticky="w", padx=10)
    combo_porte = ttk.Combobox(
        inner_frame,
        textvariable=dc.variaveis["var_porte"],
        values=list(imagens_portes.keys()),
        state="readonly"
    )
    combo_porte.grid(row=1, column=1, padx=10)
    combo_porte.set("Selecione")

    # Combobox Raça
    ttk.Label(inner_frame, text="Raça:").grid(row=2, column=0, sticky="w", padx=10)
    combo_raca = ttk.Combobox(
        inner_frame,
        textvariable=dc.variaveis["var_raca"],
        values=list(caracteristicas_racas.keys()),
        state="readonly"
    )
    combo_raca.grid(row=2, column=1, padx=10)
    combo_raca.set("Selecione")





    # # Combobox Porte
    # ttk.Label(inner_frame, text="Porte:").grid(row=1, column=0, sticky="w", padx=10)
    # combo_porte = ttk.Combobox(inner_frame, textvariable=var_porte, values=list(imagens_portes.keys()), state="readonly")
    # combo_porte.grid(row=1, column=1, padx=10)
    # combo_porte.set("Selecione")
    #
    # # Combobox Raça
    # ttk.Label(inner_frame, text="Raça:").grid(row=2, column=0, sticky="w", padx=10)
    # combo_raca = ttk.Combobox(inner_frame, textvariable=var_raca, values=list(caracteristicas_racas.keys()), state="readonly")
    # combo_raca.grid(row=2, column=1, padx=10)
    # combo_raca.set("Selecione")

    # Imagem do porte
    img_porte_label = tk.Label(inner_frame, text="Imagem do porte")
    img_porte_label.grid(row=3, column=0, padx=10, pady=5)

    # Imagem da raça
    img_raca_label = tk.Label(inner_frame, text="Imagem da raça")
    img_raca_label.grid(row=3, column=1, padx=10, pady=5)

    # Características
    label_info = tk.Label(inner_frame, text="Características da raça aparecerão aqui", font=("Segoe UI", 10),
                          bg="#f0f0f0", justify="left", relief="groove", width=60, height=5, anchor="nw")
    label_info.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    # Atualização automática de imagens e texto
    def atualizar_imagem_porte(*args):
        #porte = var_porte.get()
        porte = dc.variaveis["var_porte"].get()
        caminho = f"imagensipojucao/{imagens_portes.get(porte, '')}"
        if os.path.exists(caminho):
            img = Image.open(caminho).resize((160, 160))
            img_porte_label.imgtk = ImageTk.PhotoImage(img)
            img_porte_label.config(image=img_porte_label.imgtk)
        else:
            img_porte_label.config(image="", text="(Sem imagem)")

    def atualizar_raca_info(*args):
        #raca = var_raca.get()
        raca = dc.variaveis["var_raca"].get()
        caminho = f"imagensipojucao/{imagens_racas.get(raca, '')}"
        if os.path.exists(caminho):
            img = Image.open(caminho).resize((160, 160))
            img_raca_label.imgtk = ImageTk.PhotoImage(img)
            img_raca_label.config(image=img_raca_label.imgtk)
        else:
            img_raca_label.config(image="", text="(Sem imagem)")

        info = caracteristicas_racas.get(raca)
        if info:
            texto = f"Peso: {info['peso']}\nTamanho: {info['tamanho']}\nTemperamento: {info['temperamento']}"
        else:
            texto = "Selecione uma raça para ver suas características."
        label_info.config(text=texto)

    var_porte.trace_add("write", atualizar_imagem_porte)
    var_raca.trace_add("write", atualizar_raca_info)


# ABA CADASTRO REFORMULADA, PARTE 2:

    # Funções para seleção de imagem
    def selecionar_imagem_pet(frame_destino):
        caminho = tk.filedialog.askopenfilename(title="Selecionar imagem do PET", filetypes=[("Imagens", "*.jpg *.png")])
        if caminho:
            salvar_imagem_com_id("pet", id_pet, caminho)
            img = Image.open(caminho).resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(frame_destino, image=img_tk)
            label_img.image = img_tk  # manter referência
            label_img.grid(row=0, column=2, rowspan=4, padx=10, pady=5)
            mostrar_mascote_expressivo(janela, expressao="positivo")  # Ou "relatorio"

    def selecionar_imagem_tutor(frame_destino):
        caminho = tk.filedialog.askopenfilename(title="Selecionar imagem do Tutor", filetypes=[("Imagens", "*.jpg *.png")])
        if caminho:
            img = Image.open(caminho).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(frame_destino, image=img_tk)
            label_img.image = img_tk
            label_img.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

    # 🐶 Dados do PET
    frame_pet = ttk.LabelFrame(inner_frame, text="🐾 Dados do PET", padding=10)
    frame_pet.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    tk.Label(frame_pet, text="Nome do PET:").grid(row=0, column=0, sticky="w", padx=5)
    entry_nome_pet = tk.Entry(frame_pet, width=30)
    entry_nome_pet.grid(row=0, column=1, padx=5)

    tk.Label(frame_pet, text="Idade (anos):").grid(row=1, column=0, sticky="w", padx=5)
    entry_idade_anos = tk.Entry(frame_pet, width=5)
    entry_idade_anos.grid(row=1, column=1, sticky="w", padx=5)

    tk.Label(frame_pet, text="Idade (meses):").grid(row=1, column=2, sticky="w", padx=5)
    entry_idade_meses = tk.Entry(frame_pet, width=5)
    entry_idade_meses.grid(row=1, column=3, sticky="w", padx=5)

    tk.Label(frame_pet, text="Data do cadastro:").grid(row=2, column=0, sticky="w", padx=5)
    data_cadastro = DateEntry(frame_pet, year=2025, locale='pt_BR')
    data_cadastro.grid(row=2, column=1, padx=5, pady=5)

def rodape_imagem(frame_pai):
    caminho_img = os.path.join("imagensipojucao", "rodape", "footer.png")
    if os.path.exists(caminho_img):
        img = Image.open(caminho_img).resize((1000, 80))
        img_tk = ImageTk.PhotoImage(img)
        rodape = tk.Label(frame_pai, image=img_tk)
        rodape.image = img_tk  # mantém referência da imagem

        # Posiciona no final da grid
        rodape.grid(row=999, column=0, columnspan=999, sticky="ew")  # usa row "alta" para evitar conflito
    else:
        print("Imagem do rodapé não encontrada.")

def chamar_aba_cadastro(notebook):
    frame = criar_aba_cadastro(notebook)
    notebook.add(frame, text="Cadastro")

#barra_audio(frame_aba_cadastro)  # ou frame_aba_menu, frame_aba_config, etc.



#((((((((((((((((((((((((((()))))))))))))))))))))))))))

#(((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))

#((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))

# def atualizar_inf_porte_preco():
#     porte = dc.dc.varporte.get()
#     preco_banho = dc.dados_pet.get(porte, {}).get("preços", {}).get("Banho", 0)
#     print(f"Banho para porte {porte} custa R$ {preco_banho}")
#
#
# # def montar_aba_cadastro(aba):
# #     from dados_compartilhados import var_raca,caracteristicas_racas
# #
# #     info = caracteristicas_racas.get(var_raca.get(), {})
# #     # Use o info para configurar os campos ou exibir dados
# #
# #     titulo_aba = tk.Label(aba, text="Cadastro de PETs", font=("Segoe UI", 16))
# #     titulo_aba.pack(pady=10)
# #
# #     frame_central = ttk.LabelFrame(aba, text="Informações do Pet")
# #     frame_central.pack(fill="both", expand=True)
# #     import tkinter as tk
# #     from tkinter import ttk
# #     from dados_compartilhados import var_raca, caracteristicas_racas
#
#
#
#
#
# # def montar_aba_cadastro(aba):
# #         # 🏷️ Título da aba
# #     titulo = tk.Label(aba, text="Cadastro de PETs", font=("Segoe UI", 16))
# #     titulo.pack(pady=10)
# #
# #         # 🗂️ Frame agrupado para dados do PET
# #     frame_pet = ttk.LabelFrame(aba, text="🐶 Dados do Pet", padding=10)
# #     frame_pet.pack(fill="x", padx=20, pady=10)
# #
# #         # 📋 Combobox de seleção de raça
# #     tk.Label(frame_pet, text="Raça:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
# #     racas_disponiveis = list(caracteristicas_racas.keys())
# #     combo_racas = ttk.Combobox(frame_pet, textvariable=var_raca, values=racas_disponiveis, state="readonly",
# #                                    width=30)
# #     combo_racas.grid(row=0, column=1, padx=5, pady=5)
# #     combo_racas.set("Selecione")
# #
# #         # 📖 Label para exibir características da raça
# #     info_texto = "Características da raça aparecerão aqui."
# #     label_info = tk.Label(frame_pet, text=info_texto, font=("Segoe UI", 11), justify="left", anchor="w",
# #                               background="#f9f9f9", relief="sunken", width=50, height=5)
# #     label_info.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# #
# #         # 🔄 Função que atualiza as características dinamicamente
# # def atualizar_info_raca(*args):
# #     raca = var_raca.get()
# #     info = caracteristicas_racas.get(raca)
# #     if info:
# #             texto = f"Peso: {info['peso']}\nTamanho: {info['tamanho']}\nTemperamento: {info['temperamento']}"
# #     else:
# #             texto = "Selecione uma raça para ver suas características."
# #     label_info.config(text=texto)
# #
# #         # 🔁 Ativando trace na variável var_raca
# #     var_raca.trace_add("write", atualizar_info_raca)
# #
# #         # 🔒 Espaço reservado para expansão futura (Ex: Imagem da raça, Porte, Tipo de pelo, etc.)
# #     frame_extra = ttk.LabelFrame(aba, text="🔧 Campos adicionais", padding=10)
# #     frame_extra.pack(fill="both", expand=True, padx=20, pady=10)
#
#     # tk.Label(frame_extra, text="(Em breve: porte, tipo de pelo, pacote de serviços...)",
#     #              font=("Segoe UI", 10)).pack(pady=5)
#
#     # import tkinter as tk
#     # from tkinter import ttk
#     # from PIL import Image, ImageTk
#     # import os
#
# from dados_compartilhados import (
#     var_porte, var_raca, caracteristicas_racas,
#     imagens_portes, imagens_racas
# )
#
# def montar_aba_cadastro(aba):
#     aba.grid_columnconfigure(0, weight=1)
#     aba.grid_columnconfigure(1, weight=1)
#
#         # 🏷️ Título
#     titulo = tk.Label(aba, text="Cadastro de PETs", font=("Segoe UI", 16))
#     titulo.grid(row=0, column=0, columnspan=2, pady=10)
#
#         # 🗂️ Combobox para porte
#     tk.Label(aba, text="Porte:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
#     combo_porte = ttk.Combobox(aba, textvariable=var_porte, values=list(imagens_portes.keys()), state="readonly",
#                                    width=20)
#     combo_porte.grid(row=1, column=1, sticky="w", padx=10, pady=5)
#     combo_porte.set("Selecione")
#
#         # 🗂️ Combobox para raça
#     tk.Label(aba, text="Raça:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
#     combo_raca = ttk.Combobox(aba, textvariable=var_raca, values=list(caracteristicas_racas.keys()),
#                                   state="readonly", width=30)
#     combo_raca.grid(row=2, column=1, sticky="w", padx=10, pady=5)
#     combo_raca.set("Selecione")
#
#         # 🖼️ Imagem do porte
#     img_porte_label = tk.Label(aba, text="Imagem do porte")
#     img_porte_label.grid(row=3, column=0, padx=10, pady=5)
#
#         # 🐕 Imagem da raça
#     img_raca_label = tk.Label(aba, text="Imagem da raça")
#     img_raca_label.grid(row=3, column=1, padx=10, pady=5)
#
#         # 📋 Texto de características
#     label_info = tk.Label(
#         aba,
#         text="Características da raça aparecerão aqui.",
#         font=("Segoe UI", 11),
#         justify="left",
#         anchor="nw",
#         width=60,
#         height=5,
#         relief="groove",
#         bg="#f9f9f9"
#     )
#     label_info.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")
#
#         # 🔄 Atualiza imagem do porte
#     def atualizar_imagem_porte(*args):
#         porte = var_porte.get()
#         caminho = f"imagensipojucao/{imagens_portes.get(porte, '')}"
#         if os.path.exists(caminho):
#             img = Image.open(caminho).resize((160, 160))
#             img_porte_label.imgtk = ImageTk.PhotoImage(img)
#             img_porte_label.config(image=img_porte_label.imgtk)
#         else:
#             img_porte_label.config(image="", text="(Sem imagem)")
#
#         # 🔄 Atualiza imagem e características da raça
#     def atualizar_raca_e_info(*args):
#         raca = var_raca.get()
#
#             # Imagem da raça
#         caminho = f"imagensipojucao/{imagens_racas.get(raca, '')}"
#         if os.path.exists(caminho):
#             img = Image.open(caminho).resize((160, 160))
#             img_raca_label.imgtk = ImageTk.PhotoImage(img)
#             img_raca_label.config(image=img_raca_label.imgtk)
#         else:
#             img_raca_label.config(image="", text="(Sem imagem)")
#
#             # Texto das características
#         info = caracteristicas_racas.get(raca)
#         if info:
#             texto = f"Peso: {info['peso']}\nTamanho: {info['tamanho']}\nTemperamento: {info['temperamento']}"
#         else:
#             texto = "Selecione uma raça para ver suas características."
#         label_info.config(text=texto)
#
#         # 🔁 Trace nas variáveis
#     var_porte.trace_add("write", atualizar_imagem_porte)
#     var_raca.trace_add("write", atualizar_raca_e_info)
#
#     # Canvas + Scrollbar
#     canvas = tk.Canvas(aba)
#     scrollbar_y = ttk.Scrollbar(aba, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=scrollbar_y.set)
#
#     canvas.grid(row=0, column=0, sticky="nsew")
#     scrollbar_y.grid(row=0, column=1, sticky="ns")
#
#     # Frame rolável
#     inner_frame = ttk.Frame(canvas)
#     canvas.create_window((0, 0), window=inner_frame, anchor="nw")
#
#     def ajustar_scroll(event):
#         canvas.configure(scrollregion=canvas.bbox("all"))
#     inner_frame.bind("<Configure>", ajustar_scroll)
#
#     # === A partir daqui, crie widgets dentro do inner_frame ===
#
#     # Exemplo básico
#     frame_exemplo = ttk.LabelFrame(inner_frame, text="Seção de Exemplo")
#     frame_exemplo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
#     ttk.Label(frame_exemplo, text="Alguma informação importante").grid(row=0, column=0, sticky="w")
#
#     # Repita quantos blocos quiser (outros frames, grids, entradas, etc.)
#
#     # Se quiser ativar algo quando o porte mudar
#     dc.var_porte.trace_add("write", lambda *args: atualizar_exemplo())
#
# def atualizar_exemplo():
#     porte = dc.var_porte.get()
#     print(f"Porte selecionado na aba é: {porte}")
# # Criando o frame principal para dados cadastrais
# frame_cadastro = ttk.dc.labelFrame(inner_frame, text="Dados Cadastrais")
# frame_cadastro.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")
#
#
#
# #Calendário Cadastrar Item
# def cadastrar_item():
#     data = dc.calendario_cadastro.get_date()
#     print(f"Data cadastrada  {data}")  # Substitua por lógica de salvar o item
#     dc.label_resultado.config(text=f"Data cadastrada  {data}")
#
# # Configuração para expandir corretamente
# #aba_cadastro.columnconfigure(0, weight=1)
#
# # Frame para Data do Cadastro
# frame_dc.calendario_cadastro = ttk.dc.labelFrame(inner_frame, text="Calendario Cadastro")
# frame_dc.calendario_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# dc.calendario_cadastro = DateEntry(frame_dc.calendario_cadastro, year=2025, locale='pt_br')
# dc.calendario_cadastro.grid(row=0, column=0 , padx=10, pady=10, sticky='nsew')
#
# # Criando um Frame para Dados Cadastrais
# # frame_cadastramento = ttk.dc.labelFrame(aba_cadastro, text="Dados dos Cadastrais")
# # frame_cadastramento.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
#
# def criar_frame_cadastro(parent, text="Dados Cadastrais"):
#     frame_cadastro = ttk.dc.labelFrame(parent, )
#     frame_cadastro.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#
#     frame_cadastro = ttk.dc.label(inner_frame, "Dados Cadastrais").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
#
#     def selecionar_imagem_pet(id_pet, frame_destino):
#         caminho = filedialog.askopenfilename(title="Selecionar imagem do PET",
#                                              filetypes=[("Imagens", "*.jpg *.png")])
#         if caminho:
#             destino = os.path.join("imagens/pets", f"pet_{id_pet}.jpg")
#             shutil.copy(caminho, destino)
#
#             img = Image.open(destino).resize((150, 150))
#             img_tk = ImageTk.PhotoImage(img)
#             label_img = tk.Label(frame_destino, image=img_tk)
#             label_img.image = img_tk
#             label_img.grid(row=0, column=5, padx=5, pady=5, sticky="ne")
#
#     def mostrar_imagem_tutor(frame, tutor_id, linha, coluna):
#         caminho_imagem_tutor = os.path.join("imagens/tutores", f"tutor_{tutor_id}.jpg")
#         if os.path.exists(caminho_imagem_tutor):
#             img = Image.open(caminho_imagem_tutor).resize((60, 60))
#             img_tk = ImageTk.PhotoImage(img)
#             label_img_tutor = tk.Label(frame, image=img_tk)
#             label_img_tutor.image = img_tk
#             label_img_tutor.grid(row=linha, column=coluna, padx=5, pady=5, sticky='w')
#
#     # nome Pet
#     ttk.dc.label(inner_frame, text="Nome do Pet", anchor='w').grid(row=1, column=0, padx=10, pady=5, sticky='ew')
#     dc.entry_nome = tk.Entry(frame_cadastramento)
#     dc.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
#
#     # idade
#     ttk.dc.label(inner_frame, text="Idade Anos").grid(row=2, column=0, padx=10, pady=10, sticky='w')
#     dc.entry_idadedopetanos = ttk.Entry(inner_frame)
#     dc.entry_idadedopetanos.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
#
#     ttk.dc.label(aba_cadastro, text="Meses").grid(row=3, column=0, padx=10, pady=5, sticky='w')
#     dc.entry_idadedopetmeses = ttk.Entry(inner_frame)
#     dc.entry_idadedopetmeses.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
#
#     # Tutor 1
#     ttk.dc.labelFrame(inner_frame, text="Tutor 1").grid(row=4, column=0, padx=10, pady=10, sticky='w')
#     dc.entry_tutor_1 = tk.Entry(inner_frame)
#     dc.entry_tutor_1.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
#
#     # telefone1
#     ttk.dc.label(inner_frame, text="Telefone Tutor 1", anchor='e').grid(row=5, column=0, padx=10, pady=5, sticky='w')
#     dc.entry_telefone_1 = tk.Entry(inner_frame)
#     dc.entry_telefone_1.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#     # email Tutor1
#     ttk.dc.label(aba_cadastro, text="email Tutor 1", anchor='e').grid(row=2, column=0, padx=10, pady=10, sticky='w')
#     dc.entry_email_tutor_1 = tk.Entry(inner_frame)
#     dc.entry_email_tutor_1.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
#
#     #tutor 2
#     # ttk.dc.label(aba_cadastro, text="Tutor 2", anchor='e').grid(row=3, column=0, padx=10, pady=5, sticky='ew')
#     # # Campo de entrada (Entry)
#     # dc.entry_tutor_2 = tk.Entry(aba_cadastro)
#     # dc.entry_tutor_2.grid(row=7, column=1, padx=10, pady=10, sticky='ew')
#
#     # Tutor 2
#     frame_tutor2 = ttk.dc.labelFrame(inner_frame, text="Tutor 2")
#     frame_tutor2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
#
#     ttk.dc.label(frame_tutor2, text="Nome do Tutor").grid(row=0, column=0, padx=10, pady=5, sticky='w')
#     dc.entry_tutor_2 = tk.Entry(frame_tutor2)
#     dc.entry_tutor_2.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
#
#     #telefone 2
#     ttk.dc.label(frame_tutor2, text="Telefone Tutor 2", anchor='e').grid(row=1, column=1, padx=10, pady=5, sticky='ew')
#     # Campo de entrada (Entry)
#     dc.entry_telefone_2 = tk.Entry(inner_frame)
#     dc.entry_telefone_2.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
#     frame_telefone_2a = ttk.dc.labelFrame(inner_frame, text="Telefone_a", borderwidth=1, relief='solid')
#     dc.entry_telefone_2a = tk.Entry(inner_frame)
#     dc.entry_telefone_2a.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
#
#     #email Tutor2
#     frame_email_tutor_2 = ttk.dc.labelFrame(inner_frame, text="email Tutor 2", anchor='w')
#     frame_email_tutor_2.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
#     dc.entry_email_tutor_2 = tk.Entry(inner_frame)
#     dc.entry_email_tutor_2.grid(row=10, column=0, padx=10, pady=10, sticky='nsew')
#
#     # Criando um Frame para Endereço e Observações
#     ttk.dc.label(inner_frame, text="Endereço e Observações").grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
#     #logradouro.config(height=170)  # Define a altura manualmente
#
#     #frame_logradouro.grid_propagate(False)  # Impede que os widgets internos alterem o tamanho do frame
#
#
#     #Endereço Logradouro
#     ttk.dc.label(inner_frame, text="Endereço").grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     dc.entry_enderecopet = tk.Entry(inner_frame)
#     dc.entry_enderecopet.grid(row=2, column=1, padx=10, pady=10, sticky='nsew', columnspan=2)
#     #dc.entry_nome.grid(row=1, column=0, columnspan=4, pady=1, sticky='nsew')
#
#     #endereço Número
#     frame_endereconumero = ttk.dc.label(inner_frame, text="Número", anchor='e')
#     frame_endereconumero.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     dc.entry_endereconumero = tk.Entry(inner_frame)
#     dc.entry_endereconumero.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')
#
#     #Endereço Complemento
#     frame_enderecocomplemento = ttk.dc.label(inner_frame, text="Complemento", anchor='e')
#     frame_enderecocomplemento.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     dc.entry_enderecocomplemento = tk.Entry(inner_frame)
#     dc.entry_enderecocomplemento.grid(row=4, column=2, padx=10, pady=10, sticky='nsew')
#
#
#
#     frame_recomendacoes = ttk.dc.label(inner_frame, text="Recomendações", borderwidth=1, relief='solid')
#     frame_recomendacoes.grid(row=20, column=0, columnspan=2, padx=10, pady=5, sticky="w")
#
#     # Observações sobre o PET
#     frame_recomendacoes = ttk.dc.label(inner_frame, text="Recomendações Sobre o pet", borderwidth=1, relief='solid' )
#     frame_recomendacoes.grid(row=21, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
#     # Campo de entrada (Entry)
#     campo_observacoes = tk.Text(inner_frame, width=80, height=12, borderwidth=2, relief='solid' )
#     campo_observacoes.grid(row=30, column=0, columnspan=2, padx=10, pady=10)
#
#     # Configuração para expandir corretamente
#     janela.columnconfigure(0, weight=1)
#     janela.rowconfigure(0, weight=1)
#     aba_cadastro.columnconfigure(1, weight=1)
# #=
#
# # dc.entry_recomendacoes = tk.Entry(frame_recomendacoes)
# # dc.entry_recomendacoes.grid(row=0, column=3, padx=10, pady=10, sticky='nsew', columnspan=3)
#
# # #Criando um Frame para Endereço e Observações
# # frame_recomendacoes = ttk.dc.labelFrame(inner_frame, text="Recomendações Sobre o PET")
# # frame_cadastro.grid(row=2, column=5, columnspan=6, padx=10, pady=5, sticky="nsew")
# # dc.label_relatorio = tk.dc.label(frame_relatorio, text="Recomendações", borderwidth=1, relief='solid' )
# # #Campo para exibir o relatório
# # campo_observacoes = tk.Text(frame_cadastro, width=50, height=10, borderwidth=2, relief='solid' )
# # campo_observacoes.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
#
#
# # Criando um Frame para Dados Cadastrais
# frame_cadastramento = tk.dc.labelFrame(inner_frame, text="Dados Cadastrais", borderwidth=3, relief='groove')
# frame_cadastramento.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
# # Nome do Pet
# ttk.dc.label(frame_cadastramento, text="Nome do Pet:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
# dc.entry_nome_pet = ttk.Entry(frame_cadastramento)
# dc.entry_nome_pet.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
#
# # Idade
# ttk.dc.label(frame_cadastramento, text="Idade (Anos):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
# dc.entry_idade_anos = ttk.Entry(frame_cadastramento)
# dc.entry_idade_anos.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
#
# ttk.dc.label(frame_cadastramento, text="Idade (Meses):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
# dc.entry_idade_meses = ttk.Entry(frame_cadastramento)
# dc.entry_idade_meses.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
#
# # Criando um Frame para Endereço e Observações
# frame_endereco = tk.dc.labelFrame(inner_frame, text="Endereço e Observações", borderwidth=3, relief='groove')
# frame_endereco.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
#
# ttk.dc.label(frame_endereco, text="Endereço:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
# dc.entry_expande = ttk.Entry(frame_endereco)
# dc.entry_expande.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
#
# # aumentando o tamanho do entry configurando columnconfigure(1, weight=1)
# frame_endereco.columnconfigure(1, weight=2)
#
# # Configura as colunas do frame_endereco para expansão
# # for col in range(2):
# #     frame_endereco.columnconfigure(col, weight=1)
#
#
#
# ttk.dc.label(frame_endereco, text="Número:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
# dc.entry_fixo = ttk.Entry(frame_endereco)
# dc.entry_fixo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
#
# # Endereço Complemento
# ttk.dc.label(frame_endereco, text="Complemento").grid(row=2, column=0, padx=10, pady=10, sticky='nsew')     # Campo de entrada (Entry)
# dc.entry_enderecocomplemento = ttk.Entry(frame_endereco)
# dc.entry_enderecocomplemento.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='ew')
#
#
#
# # Criando um Frame para Dados Cadastrais
# frame_tutor = tk.dc.labelFrame(inner_frame, text="Dados dos Tutores", borderwidth=3, relief='groove')
# frame_tutor.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
#
# # Tutor 1
# ttk.dc.label(frame_tutor, text="NOME Tutor 1:").grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
# dc.entry_tutor_1 = tk.Entry(frame_tutor)
# dc.entry_tutor_1.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
#
# # telefone1
# ttk.dc.label(frame_tutor, text="Telefone Tutor 1").grid(row=4, column=0, padx=10, pady=10, sticky='e')
# dc.entry_telefone_1 = tk.Entry(frame_tutor)
# dc.entry_telefone_1.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
#
# # email Tutor1
# ttk.dc.label(frame_tutor, text="email Tutor 1").grid(row=5, column=0, padx=10, pady=10, sticky='e')
# dc.entry_email_tutor_1 = tk.Entry(frame_tutor)
# dc.entry_email_tutor_1.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')
#
# # tutor 2
# ttk.dc.label(frame_tutor, text="NOME Tutor 2:").grid(row=6, column=0, padx=10, pady=10, sticky='nsew')
#
# # Campo de entrada (Entry)
# dc.entry_tutor_2 = tk.Entry(frame_tutor)
# dc.entry_tutor_2.grid(row=6, column=1, padx=10, pady=10, sticky='nsew')
#
# # telefone 2
# ttk.dc.label(frame_tutor, text="Telefone Tutor 2").grid(row=7, column=0, padx=10, pady=10, sticky='nsew')
# # Campo de entrada (Entry)
# dc.entry_telefone_2 = tk.Entry(frame_tutor)
# dc.entry_telefone_2.grid(row=7, column=1, padx=10, pady=10, sticky='nsew')
# ttk.dc.labelFrame(frame_tutor, text="Telefone_a")
# dc.entry_telefone_2a = tk.Entry(aba_cadastro)
# dc.entry_telefone_2a.grid(row=8, column=0, padx=10, pady=10, sticky='nsew')
#
# # email Tutor2
# ttk.dc.label(frame_tutor, text="email Tutor 2").grid(row=9, column=0, padx=10, pady=10, sticky='e')
# dc.entry_email_tutor_2 = tk.Entry(frame_tutor)
# dc.entry_email_tutor_2.grid(row=9, column=1, padx=10, pady=10, sticky='nsew')
#
#
#
# # Configuração para expandir corretamente
# # janela.columnconfigure(0, weight=1)
# # janela.rowconfigure(0, weight=1)
# # aba_cadastro.columnconfigure(1, weight=1)
#
# # Criando um frame para tipopelo e Características do PET
# # frame_descricao = tk.dc.labelFrame(aba_cadastro, text="tipopelo e Características - Pelagem", borderwidth=3, relief='groove')
# # frame_descricao.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
#
# # ALTERAÇÃO COPILOT
#
# # Criando um Frame para tipopelo e Características
# aba_cadastro = ttk.Frame(inner_frame)
# aba_cadastro.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
#
# frame_descricao = tk.dc.labelFrame(inner_frame, text=" Tamanho e Características - Pelagem ", borderwidth=3, relief="groove")
# frame_descricao.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
#
# # Criando variável para os Radiobuttons
# dc.vardescricao = tk.StringVar(value="") # Inicializa sem nenhuma seleção
#
# # ALTERAÇÃO COPITOL
#
#
# # Botões de Características - Pelagem (inicialmente desabilitados)
# radiobutton_curta = tk.Radiobutton(frame_descricao, text="Curta", variable=dc.vardescricao, value="Curta")
# radiobutton_curta.grid(row=2, column=0, sticky="w")
#
# radiobutton_mediana = tk.Radiobutton(frame_descricao, text="Mediana", variable=dc.vardescricao, value="Mediana")
# radiobutton_mediana.grid(row=3, column=0, sticky="w")
#
# radiobutton_longa = tk.Radiobutton(frame_descricao, text="Longa", variable=dc.vardescricao, value="Longa")
# radiobutton_longa.grid(row=4, column=0, sticky="w")
#
# # Função para ativar/desativar Radiobuttons
#
# def atualizar_descricao():
#     if dc.vardescricao.get() in ["Curta", "Mediana", "Longa"]:
#         radiobutton_curta.config(state="normal")
#         radiobutton_mediana.config(state="normal")
#         radiobutton_longa.config(state="normal")
#     else:
#         dc.vardescricao.set("")  # Resetar seleção
#         radiobutton_curta.config(state="disabled")
#         radiobutton_mediana.config(state="disabled")
#         radiobutton_longa.config(state="disabled")
#
# # def atualizar_descricao():
# #     global dc.vardescricao  # Declare a variável como global
# #     if dc.vardescricao.get() in ["Curta", "Mediana", "Longa"]:
# #         # Ativar botões de pagamento
# #         radiobutton_curta.config(state="normal")
# #         radiobutton_mediana.config(state="normal")
# #         radiobutton_longa.config(state="normal")
# #     else:
# #         # Resetar e desabilitar botões de pagamento
# #         dc.vardescricao.set("") # Ressetar seleção
# #         radiobutton_curta.config(state="disabled")
# #         radiobutton_mediana.config(state="disabled")
# #         radiobutton_longa.config(state="disabled")
#
#
# # Botão para testar ativação dos Radiobuttons
# # btn_ativar = ttk.Button(frame_descricao, text="Ativar Seleção", command=atualizar_descricao)
# # btn_ativar.grid(row=5, column=0, pady=10, sticky="w")
#
# # Criando um Frame para Tipos de Pelos
# aba_cadastro = ttk.Frame(inner_frame)
# aba_cadastro.grid(row=4, column=0, padx=10, pady=5, sticky="w")
#
# frame_tipopelo = tk.dc.labelFrame(inner_frame, text="Tipo de Pelo", borderwidth=3, relief="groove")
# frame_tipopelo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
#
# # Criando variável para os Radiobuttons
# dc.vartipopelo = tk.StringVar(value="") # Inicializa sem nenhuma seleção
# #
# # # ALTERAÇÃO COPITOL
# #
# #
# # # Botões de forma de pagamento (inicialmente desabilitados)
# radiobutton_grosso = tk.Radiobutton(frame_tipopelo, text="Grosso Espesso", variable=dc.vartipopelo, value="Grosso Espesso")
# radiobutton_grosso.grid(row=0, column=0, sticky="w")
#
# radiobutton_fino = tk.Radiobutton(frame_tipopelo, text="Fino Suave", variable=dc.vartipopelo, value="Fino Suave")
# radiobutton_fino.grid(row=1, column=0, sticky="w")
#
#
# # Função para ativar/desativar Radiobuttons
# def atualizar_tipopelo():
#     if dc.vartipopelo.get() in ["Grosso", "Fino"]:
#         # Ativar botões de pagamento
#         radiobutton_grosso.config(state="normal")
#         radiobutton_fino.config(state="normal")
#
#     else:
#         # Resetar e desabilitar botões de pagamento
#         dc.vartipopelo.set("") # Ressetar seleção
#         radiobutton_grosso.config(state="disabled")
#         radiobutton_fino.config(state="disabled")
#
# # Botão para testar ativação dos Radiobuttons
# # btn_ativar = ttk.Button(frame_tipopelo, text="Ativar Seleção", command=atualizar_tipopelo)
# # btn_ativar.grid(row=4, column=3, pady=10, sticky="w")
#
#
# # Função para salvar no banco de dados
#     def salvar_dados_tipopelo():
#         if dc.vartipopelo.get() in ["Grosso", "Fino"]:
#             # lógica de salvamento ou processamento
#             print("Tipo de pelo selecionado:", dc.vartipopelo.get())
#         else:
#             print("Nenhum tipo de pelo válido selecionado.")
#
#
#
#     if tipopelo_selecionada:
#         conn = sqlite3.connect("petshop.db")  # Conectar ao banco de dados
#         cursor = conn.cursor()
#
#         # Criar tabela se não existir
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS caracteristicas_pet (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 descricao TEXT
#             )
#         ''')
#
#         # Inserir dados
#         cursor.execute("INSERT INTO caracteristicas_pet (descricao) VALUES (?)", (tipopelo_selecionada,))
#         conn.commit()
#         conn.close()
#
#         print(f"tipopelo '{tipopelo_selecionada}' salva no banco de dados!")
#
#
# # tempo previsto para para execução
# # Criando um Frame para Tempo de Execução
# frame_tempo = tk.dc.labelFrame(inner_frame, text="Tempo de Execução", borderwidth=3, relief='groove')
# frame_tempo.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
#
#
# # Ajustando colunas para melhor organização
# frame_tempo.grid_columnconfigure(0, weight=1)
# frame_tempo.grid_columnconfigure(1, weight=1)
#
#
# # Frame de Tempo de Execução
# ttk.dc.label(frame_tempo, text="Duração do Serviço:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
# dc.entry_duracao = tk.Entry(frame_tempo)
# dc.entry_duracao.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
#
# # Tempo Banho
# ttk.dc.label(frame_tempo, text="Tempo Banho:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
# dc.entry_banho = tk.Entry(frame_tempo)
# dc.entry_banho.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
#
#
# # Tempo Secagem
# ttk.dc.label(frame_tempo, text="Tempo Secagem:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
# dc.entry_secagem = tk.Entry(frame_tempo)
# dc.entry_secagem.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
#
#
# # Hidratação
# ttk.dc.label(frame_tempo, text="Tempo T. Hidratação:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
# dc.entry_hidratacao = tk.Entry(frame_tempo)
# dc.entry_hidratacao.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
#
#
# # Tempo Desembolo
# ttk.dc.label(frame_tempo, text="Tempo T. Desembolo:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
# dc.entry_desembolo = tk.Entry(frame_tempo)
# dc.entry_desembolo.grid(row=4, column=1, sticky="ew", padx=5, pady=2)
#
#
# # Tempo Tosa Higiênica
# ttk.dc.label(frame_tempo, text="Tempo T. Higiênica:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
# dc.entry_higienica = tk.Entry(frame_tempo)
# dc.entry_higienica.grid(row=5, column=1, sticky="ew", padx=5, pady=2)
#
# # Tempo Tosa Máquina
# ttk.dc.label(frame_tempo, text="Tempo T. Máquina:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
# dc.entry_maquina = tk.Entry(frame_tempo)
# dc.entry_maquina.grid(row=6, column=1, sticky="ew", padx=5, pady=2)
#
#
#
# # Tempo Tosa Tesoura
# ttk.dc.label(frame_tempo, text="Tempo T. Tesoura:").grid(row=7, column=0, sticky="w", padx=5, pady=2)
# dc.entry_tesoura = tk.Entry(frame_tempo)
# dc.entry_tesoura.grid(row=7, column=1, sticky="ew", padx=5, pady=2)
#
#
#
# # TEMPO TOTAL ATENDIMENTO
# ttk.dc.label(frame_tempo, text="Tempo Total Atendimento:").grid(row=8, column=0, sticky="w", padx=5, pady=2)
# dc.entry_total = tk.Entry(frame_tempo)
# dc.entry_total.grid(row=8, column=1, sticky="ew", padx=5, pady=2)
#
#
#
# tk.Button(frame_consulta, text="📷 Adicionar imagem do PET",
#           command=lambda: selecionar_imagem_pet(id_pet, frame_consulta)).grid(row=0, column=4, padx=5, pady=5)
#
# tk.Button(frame_tutor1, text="📷 Imagem Tutor 1",
#           command=lambda: selecionar_imagem_tutor(id_tutor1, frame_tutor1)).grid(row=0, column=2)
#
# mostrar_mascote_expressivo(janela, "piscando")