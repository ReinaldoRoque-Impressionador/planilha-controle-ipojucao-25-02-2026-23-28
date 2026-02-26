#importação após reestruturação do projeto
#from recursos import aba_itau
# import tkinter as tk
# from tkinter import ttk
#
# from abas.aba_clientes import montar_aba_clientes
# from modulos.interface.aba_login_fusion import criar_login
# from modulos.interface.aba_cadastro import chamar_aba_cadastro
# from modulos.abas.aba_financeiro import chamar_aba_financeiro
# from modulos.abas.aba_clientes import criar_aba_clientes
# from modulos.abas.aba_consulta import chamar_aba_consulta
# from modulos.abas.aba_relatorios import chamar_aba_relatorios
# from modulos.abas.aba_clima import montar_aba_clima
# from modulos.recursos.aba_itau import criar_aba_itau
#importações após reestruturação do projeto



# def menu_lateral(frame_principal):
#     menu = tk.Frame(frame_principal, bg="gray", width=200)
#     menu.pack(side="left", fill="y")
#
#     ttk.Button(menu, text="Login", command=criar_login).grid(row=0, column=0, sticky="ns")
#
#     ttk.Button(menu, text="Cadastro", command=chamar_aba_cadastro).grid(row=0, column=0, sticky="ns")
#     ttk.Button(menu, text="Financeiro", command=chamar_aba_financeiro).grid(row=0, column=0, sticky="ns")
#
#     ttk.Button(menu, text="Clientes", command=chamar_aba_clientes).grid(row=0, column=0, sticky="ns")
#     ttk.Button(menu, text="Consulta", command=chamar_aba_consulta).grid(row=0, column=0, sticky="ns")
#
#     ttk.Button(menu, text="Relatórios", command=chamar_aba_relatorios).grid(row=0, column=0, sticky="ns")
#
#     ttk.Button(menu, text="Clima", command=montar_aba_clima).grid(row=0, column=0, sticky="ns")
#
#     ttk.Button(menu, text="Itaú", command=criar_aba_itau).grid(row=0, column=0, sticky="ns")
#
#     # etc...


# def menu_lateral(frame_principal):
#     # Criação do menu lateral
#     menu = tk.Frame(frame_principal, bg="#d3d3d3", width=200)
#     menu.grid(row=0, column=0, sticky="ns")  # fixa na lateral esquerda
#
#     # Estilo opcional para os botões
#     estilo = ttk.Style()
#     estilo.configure("TButton", padding=6, relief="flat", background="#f0f0f0")
#
#     # Lista de botões com seus textos e comandos
#     botoes = [
#         ("Login", criar_login),
#         ("Cadastro", chamar_aba_cadastro),
#         ("Financeiro", chamar_aba_financeiro),
#         ("Clientes", montar_aba_clientes),
#         ("Consulta", chamar_aba_consulta),
#         ("Relatórios", chamar_aba_relatorios),
#         ("Clima", montar_aba_clima),
#         ("Itaú", criar_aba_itau)
#     ]
#
#     # Criação e posicionamento dos botões com grid
#     for i, (texto, comando) in enumerate(botoes):
#         btn = ttk.Button(menu, text=texto, command=comando)
#         btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
#
#     # Expansão horizontal dos botões
#     menu.grid_columnconfigure(0, weight=1)
