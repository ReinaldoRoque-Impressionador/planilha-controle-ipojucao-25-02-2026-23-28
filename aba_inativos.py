import tkinter as tk
from tkinter import ttk
from modulos.recursos import dados_compartilhados as dc
from datetime import datetime, timedelta
#from modulos.banco.db_models import Cliente, Pagamento
from modulos.banco.database import Cliente, Tutor, Usuario, Pagamento, Pets
from modulos.banco.database import database


from modulos.recursos import dados_compartilhados as dc

from modulos.recursos.som import tocar_som, tocar_som_curto, parar_som, alternar_som, continuar_som




def buscar_clientes_inativos(dias_limite=15):
    limite = datetime.today().date() - timedelta(days=dias_limite)
    clientes = database.query(Cliente).all()
    inativos = []

    for cliente in clientes:
        ultimo = (
            database.query(Pagamento)
            .filter(Pagamento.cliente_id == cliente.id)
            .order_by(Pagamento.data_pagamento.desc())
            .first()
        )
        if not ultimo or ultimo.data_pagamento < limite:
            dias = (datetime.today().date() - (ultimo.data_pagamento if ultimo else cliente.data_cadastro)).days
            inativos.append((cliente, dias))

    return inativos

def montar_aba_inativos(notebook):
    from modulos.componentes.barra_som_widget import criar_barra_som
    frame = ttk.Frame(notebook)
    frame.grid(row=0, column=0, sticky="nsew")


    ttk.Label(frame, text="Clientes Inativos", font=("Segoe UI", 14, "bold")).grid(row=0, column=0)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    ttk.Button(frame, text="📤 Exportar para Planilha", command=dc.exportar_para_planilha).grid(row=99, column=0)



    dc.variaveis["var_porte"].get()
    dc.variaveis["var_raca"].get()

    return frame
    # Frame da barra de som
    frame_barra_som = tk.Frame(frame)
    frame_barra_som.grid(row=0, column=1, sticky="nsew")

    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)

   # criar_barra_som(frame_barra_som)

    # ▶️ Botão para tocar trilha sonora longa
    # btn_trilha = ttk.Button(frame_barra_som, text="🎶 Tocar Trilha", command=lambda: tocar_som("sons/abertura.mp3"))
    # btn_trilha.grid(row=0, column=0, padx=5)

    # 🔈 Botão para tocar som curto (efeito)
    # btn_efeito = ttk.Button(frame_barra_som, text="🔔 Efeito Curto", command=lambda: tocar_som_curto("sons/sucesso.mp3"))
    # btn_efeito.grid(row=0, column=1, padx=5)
    #
    # # ⏹️ Botão para parar a trilha sonora
    # btn_parar = ttk.Button(frame_barra_som, text="🛑 Parar Música", command=parar_som)
    # btn_parar.grid(row=0, column=2, padx=5)

    # frame = ttk.LabelFrame(master, text="Clientes Inativos")
    # frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    inativos = buscar_clientes_inativos()

    for i, (cliente, dias) in enumerate(inativos):
        info = f"{cliente.nome} ({cliente.nome_pet}) - {dias} dias sem retorno"
        ttk.Label(frame, text=info).grid(row=i, column=0, sticky="w")

        ttk.Button(frame, text="Lembrar", command=lambda c=cliente: lembrar_cliente(c)).grid(row=i, column=1)
        ttk.Button(frame, text="Agendar", command=lambda c=cliente: abrir_agendamento(c)).grid(row=i, column=2)
    return inner_frame



