import socket
import threading  
import os
from classe import Sensor, Connection_device

sensor = Sensor()
connection = Connection_device()

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu():

    show_msg = 'Sistema iniciado'

    while True:
 
        show_scream(show_msg)
        option = input("\n  > ")

        # Respostas para os casos em desenvolvimento
        if (option == '1'):
            show_msg = connection.start_connection(sensor.get_commands_description())

        elif (option == '2'):
            show_msg = connection.end_connection()

        elif (option == '3'):
            show_msg = sensor.turn_on()
        
        elif (option == '4'):       
            show_msg = sensor.turn_off()
            
        elif (option == '5'):
            show_msg = sensor.get_query_data(connection.server_connected, connection.device_id)
         
        elif (option == '6'):
            show_msg = sensor.set_temperature()

        else:
            show_msg = 'Opção inválida'

        clear_terminal()

# Receber requisições do servidor (O primeiro comando funciona)
def server_request_tcp():

    while True:

        # Comando 1: get status
        # Comando 2: get descrição geral
        # Comando 3: get comandos disponíveis

        if (connection.server_connected == True):

            try:

                request = eval(connection.tcp_device.recv(2048).decode('utf-8'))
                request['Comando'] = int(request['Comando'])

                if ( not (-1 < request['Comando'] <= len(sensor.get_available_commands()) + 2)):
                    raise ValueError

                # Opções de respostas de comandos em desenvolvimento
                if (request['Comando'] == 1):

                    response_message = sensor.turn_on()
                    response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 2):

                    response_message = sensor.turn_off()
                    response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 3):
                    
                    pass

                elif (request['Comando'] == 4):
                    
                    general_description = sensor.get_general_description()
                    response = {'Tipo de resposta': 'Dicionário', 'Resposta': general_description}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 5):

                    available_commands = sensor.get_available_commands()
                    response = {'Tipo de resposta': 'Dicionário', 'Resposta': available_commands}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == -1):

                    response = 'Recebido'
                    connection.tcp_device.send(response.encode('utf-8'))

            except (ValueError) as e:
                response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': 'Comando inválido'}
                connection.tcp_device.send(str(response).encode('utf-8'))

            except (ConnectionAbortedError) as e:   # Quando o dispostivo cancela a comunicação
                pass

            except (ConnectionResetError) as e:     # Quando o servidor é encerrado
                connection.end_connection()

# Enviar os dados via UDP (parece que ta funcionando)
def send_data_udp():    

    while True:
            
        if (connection.server_ip != "" and sensor.temperature != "-----"):
            
            if (sensor.status == 'ligado'):
                data = sensor.get_returning_data()
                data['Válido'] = True
            elif (sensor.status == 'desligado'):
                data = {}
                data['Válido'] = False
                data['Justificativa'] = 'Dispositivo desligado, não é possível coletar os dados'
            connection.udp_device.sendto( str(data).encode('utf-8'), (connection.server_ip, connection.udp_port))

def show_scream( show_msg):

    print("\n+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
    print("|                            SENSOR DE TEMPERATURA                            |")
    print("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

    print('''+-----------------------------------------------------------------------------+
|                                                                             |
|                      [ 1 ]    CONECTAR AO SERVIDOR                          |
|                      [ 2 ]    DESCONECTAR DO SERVIDOR                       |
|                      [ 3 ]    LIGAR                                         |
|                      [ 4 ]    DESLIGAR                                      |
|                      [ 5 ]    CONSULTAR DADOS                               |
|                      [ 6 ]    SETAR TEMPERATURA                             |
|                                                                             |
+-----------------------------------------------------------------------------+''')

    if (type(show_msg) == str):
        len_msg = len(show_msg)
        space_beginning = (77 - len_msg) // 2
        space_ending = 77 - (space_beginning + len_msg)
        print("+-----------------------------------------------------------------------------+")
        print("|" + " " * space_beginning + show_msg + " " * space_ending + "|")
        print("+-----------------------------------------------------------------------------+")

    else:
        if (show_msg['Status'] == 'Ligado'):
            space_status = 3
        else:
            space_status = 0
        
        space_temperature = 5 - len(show_msg['Temperatura'])

        if (show_msg['Servidor'] == 'Conectado'):
            space_server = 3
        else:
            space_server = 0

        print("+-----------+-------------------+--------------------+------------------------+")
        print("| ID: " + show_msg['ID'] + " | Status: " + show_msg['Status'] + " " * space_status + " | Temperatura: " + show_msg['Temperatura'] + " " * space_temperature + " | Servidor: " + show_msg['Servidor'] + " " * space_server + " |")
        print("+-----------+-------------------+--------------------+------------------------+")

def clear_terminal():
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas (Linux, macOS)
        os.system('clear')

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp).start()
    threading.Thread(target=send_data_udp).start()
    menu()

if __name__=="__main__":
    iniciar()
