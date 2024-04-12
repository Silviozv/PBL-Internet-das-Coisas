import socket
import threading  
from classe import Sensor, Connection_device

sensor = Sensor()
connection = Connection_device()

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu():

    while True:
        
        option = input("\n[1] Conectar ao servidor\n[2] Desconectar do servidor\n[3] Ligar\n[4] Consultar dados\n[5] Setar temperatura\n[6] Desligar\n\n> ").strip()  

        # Respostas para os casos em desenvolvimento
        if (option == '1'):

            ip_servidor = input("\nIP servidor: ")

            if (connection.server_connected == False):

                try:
                    connection.tcp_device.connect( (ip_servidor, connection.tcp_port))
                    with connection.lock:
                        connection.server_ip = ip_servidor
                        connection.server_connected = True
                    print("\nConexão estabelecida")
                    
                except (ConnectionRefusedError, socket.gaierror) as e:
                    print("\nConexão impossibilitada")

            else:
                print("\nConexão já estabelecida")

        elif (option == '2'):

            if (connection.server_connected == True):

                with connection.lock:
                    connection.server_connected = False
                    connection.tcp_device.close()
                    connection.restart_tcp_connection()

                print("\nConexão encerrada")

            else:
                print("\nNão há um servidor conectado")

        elif (option == '3'):

            if sensor.status == 'desligado':

                with connection.lock:
                    sensor.status = 'ligado'

                print("\nDispositivo ligado")

            else:
                print("\nDispositivo já está ligado")
        
        elif (option == '4'):       

            print(f"\nIP local: {sensor.local_ip}")
            print(f"Descrição: {sensor.description}")
            print(f"Status: {sensor.status}")
            print(f"Temperatura: {sensor.temperature}")
            
        elif (option == '5'):

            new_temperature = int(input("\nTemperatura: "))
            with connection.lock:
                sensor.temperature = new_temperature

            print("\nTemperatura atualizada")
         
        elif (option == '6'):

            if (sensor.status == 'ligado'):
                with connection.lock:
                    sensor.status = 'desligado'
                print("\nDispositivo desligado")

            else:
                print("\nDispositivo já está desligado")

# Receber requisições do servidor (O primeiro comando funciona)
def server_request_tcp():

    while True:

        # Comando 1: get status
        # Comando 2: get descrição geral

        if (connection.server_connected == True):

            try:

                command = int(connection.tcp_device.recv(2048).decode('utf-8'))

                # Opções de respostas de comandos em desenvolvimento
                if (command == 1):

                    status = sensor.get_status()
                    connection.tcp_device.send(status.encode('utf-8'))


                elif command == 2:

                    if sensor.status == 'ligado':
                        with connection.lock:
                            sensor.status = 'desligado'
                        connection.tcp_device.send("Dispositivo desligado".encode('utf-8'))

                    else:
                        connection.tcp_device.send("Dispositivo já está desligado".encode('utf-8'))

            except (ConnectionAbortedError) as e:
                pass

# Enviar os dados via UDP (parece que ta funcionando)
def send_data_udp():    

    while True:
            
        if (connection.server_ip != ""):

            if (connection.server_connected == True and sensor.status == 'ligado'):

                data = sensor.get_returning_data()
                connection.udp_device.sendto( str(data).encode('utf-8'), (connection.server_ip, connection.udp_port))

            elif (connection.server_connected == False):

                connection.udp_device.sendto(("Conexao encerrada").encode('utf-8'), (connection.server_ip, connection.udp_port))

                with connection.lock:
                    connection.server_ip = ""

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp).start()
    threading.Thread(target=send_data_udp).start()
    menu()

iniciar()
