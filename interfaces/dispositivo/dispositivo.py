import threading  
from classe import Dispositivo, Conexao

dispositivo = Dispositivo()
conexao = Conexao()

def menu( ip_local):

    while True:
        
        opcao = int(input("\n[1] Conectar ao servidor\n[2] Desconectar do servidor\n[3] Ligar\n[4] Consultar dados\n[5] Setar temperatura\n[6] Desligar\n\n> "))   

        # Respostas para os casos em desenvolvimento
        if opcao == 1:

            conexao.ip_servidor = input("\nIP servidor: ")
            if conexao.servidor_conectado == False:

                try:
                    conexao.dispositivo_tcp.connect( (conexao.ip_servidor, conexao.porta_tcp))
                    with conexao.lock:
                        conexao.servidor_conectado = True
                    print("\nConexão estabelecida")
                    
                except ConnectionRefusedError as e:
                    print("\nConexão impossibilitada")

            else:
                print("\nConexão já estabelecida")

        elif opcao == 2:

            if conexao.servidor_conectado == True:
                with conexao.lock:
                    conexao.servidor_conectado = False
                    print("\nConexão encerrada")
            else:
                print("\nNão há um servidor conectado")

        elif opcao == 3:

            if dispositivo.status == 'desligado':
                with conexao.lock:
                    dispositivo.status = 'ligado'
                conexao.dispositivo_tcp.send("Dispositivo ligado".encode('utf-8'))

            else:
                conexao.dispositivo_tcp.send("Dispositivo já está ligado".encode('utf-8'))
        
        elif opcao == 4:       

            print("\nIP local:", dispositivo.ip_local)
            print("Status:", dispositivo.status)
            print("Temperatura:", dispositivo.temperatura)
            
        elif opcao == 5:

            nova_temperatura = int(input("Temperatura: "))
            with conexao.lock:
                dispositivo.temperatura = nova_temperatura
         
        elif opcao == 6:

            if dispositivo.status == 'ligado':
                with conexao.lock:
                    dispositivo.status = 'desligado'
                conexao.dispositivo_tcp.send("Dispositivo desligado".encode('utf-8'))

            else:
                conexao.dispositivo_tcp.send("Dispositivo já está desligado".encode('utf-8'))

# Receber requisições do servidor
def requisicao_servidor( ip_local):

    while True:

        # Comando 1: ligar sensor
        # Comando 2: desligar sensor

        if conexao.servidor_conectado == True:
            comando = int(conexao.dispositivo_tcp.recv(2048).decode('utf-8'))

            # Opções de respostas de comandos em desenvolvimento
            if comando == 1:

                if dispositivo.status == 'desligado':
                    with conexao.lock:
                        dispositivo.status = 'ligado'
                    conexao.dispositivo_tcp.send("Dispositivo ligado".encode('utf-8'))

                else:
                    conexao.dispositivo_tcp.send("Dispositivo já está ligado".encode('utf-8'))

            elif comando == 2:

                if dispositivo.status == 'ligado':
                    with conexao.lock:
                        dispositivo.status = 'desligado'
                    conexao.dispositivo_tcp.send("Dispositivo desligado".encode('utf-8'))

                else:
                    conexao.dispositivo_tcp.send("Dispositivo já está desligado".encode('utf-8'))

# Enviar os dados via UDP
def enviar_dados():    

    while True:

        if conexao.ip_servidor != "":
                
            dados = { "Descrição": "Sensor de temperatura", "Status": dispositivo.status, "Temperatura": dispositivo.temperatura}

            conexao.dispositivo_udp.sendto( str(dados).encode('utf-8'), (conexao.ip_servidor, conexao.porta_udp))
def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=requisicao_servidor, args=(dispositivo.ip_local,)).start()
    #threading.Thread(target=enviar_dados).start()
    menu(dispositivo.ip_local)

iniciar()
