import socket
import threading  

# Conectando com o servidor
porta_tcp = 5050
ip_local = socket.gethostbyname( socket.gethostname())

dispositivo_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

# Dados do dispositivo
status = 'desligado'
temperatura = 0
conexao = False

lock = threading.Lock()

def menu( ip_local):
    global status
    global temperatura
    global conexao

    while True:
        
        opcao = int(input("\n[1] Conectar ao servidor\n[2] Desconectar do servidor\n[3] Ligar\n[4] Consultar dados\n[5] Setar temperatura\n[6] Desligar\n\n> "))   

        # Respostas para os casos em desenvolvimento
        if opcao == 1:
            ip_servidor = input("\nIP servidor: ")
            if conexao == False:

                try:
                    dispositivo_tcp.connect( (ip_servidor, porta_tcp))
                    with lock:
                        conexao = True
                    print("\nConexão estabelecida")
                except ConnectionRefusedError as e:
                    print("\nConexão impossibilitada")

            else:
                print("\nConexão já estabelecida")

        elif opcao == 2:
            if conexao == True:
                with lock:
                    conexao = False
                    print("\nConexão encerrada")
            else:
                print("\nNão há um servidor conectado")

        elif opcao == 3:
            with lock:
                status = 'ligado'
        
        elif opcao == 4:       
            print("\nIP local:", ip_local)
            print("Status:", status)
            print("Temperatura:", temperatura)
            
        elif opcao == 5:
            nova_temperatura = int(input("Temperatura: "))
            with lock:
                temperatura = nova_temperatura
         
        elif opcao == 6:
            with lock:
                status = 'desligado' 

def requisicao_servidor( ip_local):
    global status
    global temperatura
    global conexao

    while True:

        if conexao == True:
            comando = int(dispositivo_tcp.recv(2048).decode('utf-8'))

            # Opções de respostas de comandos em desenvolvimento
            if comando == 1:
                with lock:
                    status = 'ligado'
                dispositivo_tcp.send("dispositivo ligado".encode('utf-8'))

            elif comando == 2:
                info = "\nIP: " + ip_local + "\nStatus: " + status + "\nTemperatura: " + str(temperatura) 
                dispositivo_tcp.send(info.encode('utf-8'))

            elif comando == 3:
                with lock:
                    status = 'desligado'

# A lógica de receber comandos e poder executar opções do menu parecem funcionar
threading.Thread(target=requisicao_servidor, args=(ip_local,)).start()
menu(ip_local)

