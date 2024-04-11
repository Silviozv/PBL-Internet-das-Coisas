import threading
from classe import Armazenamento, Conexao_servidor

# lógica embaralhada
# recebe as conexões; armazena os sockets e printa; o comando de resposta é um rascunho

# É para colocar como global?

armazenamento = Armazenamento()
conexao_servidor = Conexao_servidor()
print(conexao_servidor.ip_servidor)

# Função temporária para enviar comandos ao dispositivo !!!! MUDEI PARA DICIONARIO
def enviar_comando(endereco):

    while True:

        comando = input("\nComando: ")
        armazenamento.conexoes[endereco].send(comando.encode('utf-8'))
        print(armazenamento.conexoes[endereco].recv(2048).decode('utf-8'))

# Aceitar dispositivos que iniciam conexões (parece que funciona) 
def receber_conexao():
    
    while True:

        remetente, endereco_remetente = conexao_servidor.servidor_tcp.accept()
        armazenamento.conexoes[endereco_remetente[0]] = remetente
        print("Nova conexao:", endereco_remetente)
        enviar_comando(endereco_remetente[0])

# Receber os dados enviados por udp (parece que funciona)
def receber_dados():

    while True:

        dados, endereco = conexao_servidor.servidor_udp.recvfrom(2048)
        print(dados.decode('utf-8'))
        print(endereco[0])
        armazenamento.dados_dispositivos[endereco[0]] = dados.decode('utf-8')

def iniciar():

    threading.Thread(target=receber_dados).start()
    receber_conexao()

iniciar()