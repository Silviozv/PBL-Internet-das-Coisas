import socket
import threading  
from classe import Dispositivo, Conexao

dispositivo = Dispositivo()
conexao = Conexao()

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu():

    while True:
        
        opcao = input("\n[1] Conectar ao servidor\n[2] Desconectar do servidor\n[3] Ligar\n[4] Consultar dados\n[5] Setar temperatura\n[6] Desligar\n\n> ").strip()  

        # Respostas para os casos em desenvolvimento
        if (opcao == '1'):

            ip_servidor = input("\nIP servidor: ")

            if (conexao.servidor_conectado == False):

                try:
                    conexao.dispositivo_tcp.connect( (ip_servidor, conexao.porta_tcp))
                    with conexao.lock:
                        conexao.ip_servidor = ip_servidor
                        conexao.servidor_conectado = True
                    print("\nConexão estabelecida")
                    
                except (ConnectionRefusedError, socket.gaierror) as e:
                    print("\nConexão impossibilitada")

            else:
                print("\nConexão já estabelecida")

        elif (opcao == '2'):

            if (conexao.servidor_conectado == True):

                with conexao.lock:
                    conexao.servidor_conectado = False
                    conexao.dispositivo_tcp.close()
                    conexao.reiniciar_conexao_tcp()

                print("\nConexão encerrada")

            else:
                print("\nNão há um servidor conectado")

        elif (opcao == '3'):

            if dispositivo.status == 'desligado':

                with conexao.lock:
                    dispositivo.status = 'ligado'

                print("\nDispositivo ligado")

            else:
                print("\nDispositivo já está ligado")
        
        elif (opcao == '4'):       

            print(f"\nIP local: {dispositivo.ip_local}")
            print(f"Descrição: {dispositivo.descricao}")
            print(f"Status: {dispositivo.status}")
            print(f"Temperatura: {dispositivo.temperatura}")
            
        elif (opcao == '5'):

            nova_temperatura = int(input("\nTemperatura: "))
            with conexao.lock:
                dispositivo.temperatura = nova_temperatura

            print("\nTemperatura atualizada")
         
        elif (opcao == '6'):

            if (dispositivo.status == 'ligado'):
                with conexao.lock:
                    dispositivo.status = 'desligado'
                print("\nDispositivo desligado")

            else:
                print("\nDispositivo já está desligado")

# Receber requisições do servidor (O primeiro comando funciona)
def requisicao_servidor():

    while True:

        # Comando 1: coletar status
        # Comando 2: desligar sensor

        if (conexao.servidor_conectado == True):
            comando = int(conexao.dispositivo_tcp.recv(2048).decode('utf-8'))

            # Opções de respostas de comandos em desenvolvimento
            if (comando == 1):

                status = dispositivo.get_status()
                conexao.dispositivo_tcp.send(status.encode('utf-8'))


            elif comando == 2:

                if dispositivo.status == 'ligado':
                    with conexao.lock:
                        dispositivo.status = 'desligado'
                    conexao.dispositivo_tcp.send("Dispositivo desligado".encode('utf-8'))

                else:
                    conexao.dispositivo_tcp.send("Dispositivo já está desligado".encode('utf-8'))

# Enviar os dados via UDP (parece que ta funcionando)
def enviar_dados():    

    while True:
            
        if (conexao.ip_servidor != ""):

            if (conexao.servidor_conectado == True and dispositivo.status == "ligado"):

                dados = dispositivo.get_informacoes
                conexao.dispositivo_udp.sendto( str(dados).encode('utf-8'), (conexao.ip_servidor, conexao.porta_udp))

            elif (conexao.servidor_conectado == False):

                conexao.dispositivo_udp.sendto(("Conexao encerrada").encode('utf-8'), (conexao.ip_servidor, conexao.porta_udp))

                with conexao.lock:
                    conexao.ip_servidor = ""

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=requisicao_servidor).start()
    threading.Thread(target=enviar_dados).start()
    menu()

iniciar()
