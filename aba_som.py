import pygame
pygame.mixer.init()
import threading
import os



#✅ Etapa 1: Criar a  para centralizar os sons
#Assim você evita repetir código nas abas. Aqui vai um modelo prático:E substituir linhas como:

#✅ Etapa 2: Substituir o uso de playsound em todas as abas
#Você só precisa fazer:
#from aba_som import tocar_som, alternar_som_estado
#E substituir linhas como:
#threading.Thread(target=playsound, args=(caminho,), daemon=True).start()
# POR:
#tocar_som(caminho)


som_ativo = True  # Pode ser controlado por botão externo - # ⚙️ controle global de som

def inicializar_audio():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

def tocar_som(caminho):
    if som_ativo and os.path.exists(caminho):
        def reproduzir():
            inicializar_audio()
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()
        threading.Thread(target=reproduzir, daemon=True).start()

# 🔈 Funções específicas

def som_abertura():
    tocar_som("sons/musica_abertura.mp3")

# 🔈 Funções específicas
def som_login():
    tocar_som("sons/login.mp3")

# 🔈 Funções específicas
def som_consulta_pet():
    tocar_som("sons/musica_consulta_pet.mp3")

# 🔈 Funções específicas
def som_relatorio():
    tocar_som("sons/relatorio.mp3")

# 🔈 Funções específicas
def som_acesso_concedido():
    tocar_som("sons/acesso_concedido.mp3")

# 🔈 Funções específicas
def som_acesso_negado():
    tocar_som("sons/acesso_negado.mp3")

# 🔈 Funções específicas
def som_fechamento():
    tocar_som("sons/musica_end_of_day.mp3")

# 🔈 Funções específicas
# 🔇 Alternar som
def alternar_som_estado(botao):
    global som_ativo
    som_ativo = not som_ativo
    novo_texto = "🔈 Som Ativado" if som_ativo else "🔇 Som Desativado"
    botao.config(text=novo_texto)

def tocar_som_bloqueante(caminho):
    if som_ativo and os.path.exists(caminho):
        inicializar_audio()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)



trilhas = {
    "abertura": "som/musica_abertura.wav",
    "consulta": "som/musica_consulta.mp3",
    "salvando": "som/salvando.mp3",
    "clientes": "som/clair_de_lune_prelude.mp3",
    "relatorios": "som/relatorio.mp3",
    "fechamento": "som/end_of_day.mp3",
    "usuario_adicionado": "som/lightsaber_clash_88733.mp3",
    "usuario_removido": "som/lightsaber4_87668.mp3"


}

def tocar_trilha(nome):
    caminho = trilhas.get(nome)
    if caminho:
        tocar_som(caminho)

def tocar_som(caminho):
    if som_ativo and os.path.exists(caminho):
        def reproduzir():
            try:
                inicializar_audio()
                pygame.mixer.music.load(caminho)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Erro ao tocar som: {e}")
        threading.Thread(target=reproduzir, daemon=True).start()

def som_e_expressao_acao(acao):
    print(f"Ação: {acao} — mascote reagiu!")

# def musica_abertura():
#     tocar_som("som/musica_abertura.mp3")
#
# def lightsaber_ignition_6816():
#     tocar_som("som/lightsaber_ignition_6816.mp3")
#
# def bouncy_pet_intro():
#     tocar_som("som/bouncy_pet_intro.mp3")
#
# def clair_de_lune():
#     tocar_som("clair_de_lune.mp3")
#
# def light_sabre_77103():
#     tocar_som("som/light_sabre_77103.mp3")
#
# def lightsaber_clash_88773():
#     tocar_som("som/lightsaber_clash_88773.mp3")
#
# def end_of_day():
#     tocar_som("som/end_of_day.mp3")
#
# def musica_consulta():
#     tocar_som("som/musica_consulta.mp3")
#
# def salvando():
#     tocar_som("som/salvando.mp3")
#
# def usuario_adicionado():
#     tocar_som("som/usuario_adicionado.mp3")
#
# def usuario_removido():
#     tocar_som("som/usuario_removido.mp3")
#
# def relatorio():
#     tocar_som("som/relatorio.mp3")
#



#E quando quiser tocar uma delas:
from aba_som import tocar_som
#caminho = trilhas.get(trilha_selecionada.get())
#tocar_som(caminho)

#✅ Etapa 4: Botão para ativar/desativar som
#Substitua:

#por:
#from aba_som import alternar_som_estado
#btn_audio.config(command=lambda: alternar_som_estado(btn_audio))


#🔍 Etapa 5: Fechamento com música
#Atualize sua função:
def mostrar_despedida_e_sair():
    despedida = tk.Label(janela, text="🐾 Até logo! Obrigado por cuidar com carinho.", font=("Segoe UI", 14), fg="#444")
    despedida.place(relx=0.5, rely=0.4, anchor="center")

    caminho = os.path.join("../Planilha Controle Ipojucão/sons", "musica_end_of_day.mp3")
    tocar_som(caminho)

    def fade_out(passo=0):
        alpha = max(0, 1 - passo / 20)
        cinza = int(68 * alpha)
        cor = f"#{cinza:02x}{cinza:02x}{cinza:02x}"
        despedida.config(fg=cor)
        if passo < 20:
            janela.after(50, fade_out, passo + 1)
        else:
            janela.quit()

    janela.after(1000, fade_out)


#🎯 Comandos para usar em cada aba do sistema
#🟢 Abertura do sistema (em main.py)
#No início da função principal, chame:
# from aba_som import som_abertura
# som_abertura()


#Pode ser após o splash animado ou antes de mostrar a janela.


# 🔐 Login (em aba_login.py)
# Ao validar as credenciais:
# from aba_som import som_acesso_concedido, som_acesso_negado

# if sucesso:
#     som_acesso_concedido()
# else:
#     som_acesso_negado()



# 🧾 Consulta de PET (em aba_consulta.py)
# Quando o usuário for carregado ou exibido com sucesso:
# from aba_som import som_consulta_pet
# som_consulta_pet()



# 📊 Relatórios (em aba_relatorio.py)
# Ao gerar ou enviar um relatório:
# from aba_som import som_relatorio
# som_relatorio()



# 🛑 Fechamento do sistema
# No botão de sair ou função de encerramento:
# from aba_som import som_fechamento
# som_fechamento()



# 🔁 Botão de ativar/desativar som
# from aba_som import alternar_som_estado
# btn_audio.config(command=lambda: alternar_som_estado(btn_audio))





