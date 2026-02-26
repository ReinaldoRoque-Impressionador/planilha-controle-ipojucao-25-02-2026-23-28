
#importação após reestruturação do projeto
#expecíficamente para a aba_mensageiro

from modulos.recursos.utils_mensagens import enviar_mensagem_whatsapp
#from modulos.banco.db_models import Cliente
from modulos.banco.database import Cliente, Tutor, Usuario, Pagamento, Pets
#importação após reestruturação do projeto
#expecíficamente para a aba_mensageiro

#from modulos.banco.db_models import Cliente
#importação após reestruturação do projeto
#expecíficamente para a aba_mensageiro

import tkinter as tk
from tkinter import ttk
import pywhatkit as kit
import datetime


def criar_aba_mensageiro(master):
    frame = ttk.Frame(master)
    frame.grid(row=0, column=1, sticky="nsew")

    ttk.Label(frame, text="📨 Mensageiro", font=("Arial", 16)).pack(pady=10)

    caixa_mensagem = tk.Text(frame, height=10, width=50)
    caixa_mensagem.grid(row=1, column=0, pady=5)


    ttk.Button(frame, text="Enviar", command=lambda: print("Mensagem enviada")).pack()

    return frame





#✅ Etapa 1: Organização modular para envio de mensagens
#Vamos criar um arquivo chamado , que vai conter:
#🔹 Função para clientes — com serviços detalhados


def enviar_mensagem_cliente(cliente_id, servicos_selecionados, valores_unitarios):
    cliente = buscar_cliente_por_id(cliente_id)  # função que busca telefone e nome
    numero = cliente["telefone"]
    nome = cliente["nome"]

    # Gerar mensagem dos serviços
    texto_servicos = "🐶 Serviços prestados:\n"
    total = 0
    for servico in servicos_selecionados:
        valor = valores_unitarios.get(servico, 0)
        total += valor
        texto_servicos += f"- {servico}: R$ {valor:.2f}\n"

    texto_servicos += f"\n💰 Total: R$ {total:.2f}"

    # Enviar mensagens separadas
    mensagens = [
        f"Olá, {nome}! Aqui está o resumo do atendimento do seu PET:",
        texto_servicos,
        f"Para pagamento, enviaremos o link PIX em breve. Obrigado por confiar no Ipojucão PET SHOP!"
    ]

    for msg in mensagens:
        enviar_mensagem_whatsapp(numero, msg)


# Essa função permite adicionar qualquer novo serviço sem mudar a lógica!


#🔹 Função para administradores — relatórios livres

def enviar_relatorio_administrador(relatorio_texto, destinatarios_admin):
    for admin in destinatarios_admin:
        numero = admin["telefone"]
        mensagem = f"📋 Relatório Ipojucão:\n{relatorio_texto}"
        enviar_via_whatsapp(numero, mensagem)


# Você pode selecionar os admins em uma interface de múltipla escolha.





