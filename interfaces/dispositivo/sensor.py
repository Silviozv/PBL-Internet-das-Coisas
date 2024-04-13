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
            print(f"\n{connection.start_connection()}")

        elif (option == '2'):
            print(f"\n{connection.end_connection()}")

        elif (option == '3'):
            print(f"\n{sensor.turn_on()}")
        
        elif (option == '4'):       
            print(f"\n{sensor.get_atributes()}")
            
        elif (option == '5'):
            print(f"\n{sensor.set_temperature()}")
         
        elif (option == '6'):
            print(f"\n{sensor.turn_off()}")

# Receber requisições do servidor (O primeiro comando funciona)
def server_request_tcp():

    while True:

        # Comando 1: get status
        # Comando 2: get descrição geral
        # Comando 3: get comandos disponíveis

        if (connection.server_connected == True):

            try:

                command = int(connection.tcp_device.recv(2048).decode('utf-8'))

                # Opções de respostas de comandos em desenvolvimento
                if (command == 1):

                    available_commands = sensor.get_available_commands()
                    connection.tcp_device.send(str(available_commands).encode('utf-8'))

                elif (command == 2):

                    general_description = sensor.get_general_description()
                    connection.tcp_device.send(str(general_description).encode('utf-8'))

                elif (command == 3):
                    
                    response = sensor.turn_on()
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (command == 4):
                    
                    response = sensor.turn_off()
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (command == 5):

                    status = sensor.get_status()
                    connection.tcp_device.send(status.encode('utf-8'))

                elif (command == 6):

                    status = sensor.get_type()
                    connection.tcp_device.send(status.encode('utf-8'))

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

if __name__=="__main__":
    iniciar()
