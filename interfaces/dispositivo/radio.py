import socket
import threading  
from classe import Radio, Connection_device

radio = Radio()
connection = Connection_device()

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu():

    while True:
        
        option = input("\n[1] Conectar ao servidor\n[2] Desconectar do servidor\n[3] Ligar\n[4] Consultar dados\n[5] Setar Música\n[6] Desligar\n\n> ").strip()  

        # Respostas para os casos em desenvolvimento
        if (option == '1'):
            print(f"\n{connection.start_connection()}")

        elif (option == '2'):
            print(f"\n{connection.end_connection()}")

        elif (option == '3'):
            print(f"\n{radio.turn_on()}")
        
        elif (option == '4'):       
            print(f"\n{radio.get_atributes()}")
            
        elif (option == '5'):
            new_music = input("Música: ")
            print(f"\n{radio.set_music(new_music)}")
         
        elif (option == '6'):

            print(f"\n{radio.turn_off()}")

def server_request_tcp():

    while True:

        # Comando 1: get status
        # Comando 2: get descrição geral
        # Comando 3: get comandos disponíveis

        if (connection.server_connected == True):

            try:

                request = connection.tcp_device.recv(2048).decode('utf-8')

                request_parts = request.split()
                command = int(request_parts[0])

                # Opções de respostas de comandos em desenvolvimento
                if (command == 1):

                    available_commands = radio.get_available_commands()
                    connection.tcp_device.send(str(available_commands).encode('utf-8'))

                elif (command == 2):

                    general_description = radio.get_general_description()
                    connection.tcp_device.send(str(general_description).encode('utf-8'))

                elif (command == 3):
                    
                    response = radio.turn_on()
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (command == 4):
                    
                    response = radio.turn_off()
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (command == 5):

                    request_parts.pop(0)
                    music = ' '.join(request_parts)

                    response = radio.set_music(music)
                    connection.tcp_device.send(response.encode('utf-8'))

                elif (command == 6):

                    type = radio.get_type()
                    connection.tcp_device.send(str(type).encode('utf-8'))

            except (ConnectionAbortedError) as e:
                pass

# Enviar os dados via UDP (parece que ta funcionando)
def warning_end_connection():    

    while True:
            
        if (connection.server_ip != "" and connection.server_connected == False):

                connection.udp_device.sendto(("Conexao encerrada").encode('utf-8'), (connection.server_ip, connection.udp_port))

                with connection.lock:
                    connection.server_ip = ""

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp).start()
    threading.Thread(target=warning_end_connection).start()
    menu()

if __name__=="__main__":
    iniciar()