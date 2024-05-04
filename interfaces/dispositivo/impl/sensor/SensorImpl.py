import socket
import os
import time
import threading

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu( sensor, connection):

    show_msg = 'Sistema iniciado'

    while True:
 
        show_scream(show_msg)
        option = input("\n  > ").strip()

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
            show_msg = sensor.get_query_data(connection.server_status, connection.device_id)
         
        elif (option == '6'):
            show_msg = sensor.set_temperature()

        else:
            show_msg = 'Opção inválida'

        clear_terminal()

# Receber requisições do servidor (O primeiro comando funciona)
def server_request_tcp( sensor, connection):

    while True:

        # Comando 1: get status
        # Comando 2: get descrição geral
        # Comando 3: get comandos disponíveis

        if (connection.server_status == 'Conectado'):

            try:

                request = connection.tcp_device.recv(2048).decode('utf-8')

                if (request == ""):
                    raise ConnectionResetError
                
                request = eval(request)

                request['Comando'] = int(request['Comando'])

                if ( not (-1 < request['Comando'] <= len(sensor.get_available_commands()) + 2)):
                    raise ValueError

                # Opções de respostas de comandos em desenvolvimento
                if (request['Comando'] == 0):

                    response = 'Recebido'
                    connection.tcp_device.send(response.encode('utf-8'))

                elif (request['Comando'] == 1):

                    response_message = sensor.turn_on()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 2):

                    response_message = sensor.turn_off()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 3):
                    pass

                elif (request['Comando'] == 4):
                    
                    general_description = sensor.get_general_description()
                    response = {'Resposta': general_description}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 5):

                    available_commands = sensor.get_available_commands()
                    response = {'Resposta': available_commands}
                    connection.tcp_device.send(str(response).encode('utf-8'))

            except (ValueError) as e:
                response = {'Resposta': 'Comando inválido'}
                connection.tcp_device.send(str(response).encode('utf-8'))

            except (ConnectionAbortedError, ConnectionResetError, OSError, socket.timeout) as e:   # Quando o dispositivo cancela a comunicação
                if connection.server_ip != "":
                    connection.server_status = 'Reconectando'
                    threading.Thread(target=connection.loop_reconnection, args=[ sensor.get_available_commands()]).start()


# Enviar os dados via UDP (parece que ta funcionando)
def send_data_udp( sensor, connection):    

    begin = time.time()
    while True:
            
        if (connection.server_ip != "" and sensor.temperature != "-----"):
            
            if ( (time.time() - begin) >= 0.5):
                if (sensor.status == 'ligado'):
                    data = sensor.get_returning_data()
                    data['Válido'] = True
                elif (sensor.status == 'desligado'):
                    data = {}
                    data['Válido'] = False
                    data['Justificativa'] = 'Dispositivo desligado, não é possível coletar os dados'
                connection.udp_device.sendto( str(data).encode('utf-8'), (connection.server_ip, connection.udp_port))
                begin = time.time()


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
        space_id = 5 - len(show_msg['ID'])
        space_status = 9 - len(show_msg['Status'])
        space_temperature = 5 - len(show_msg['Temperatura'])
        space_server = 12 - len(show_msg['Servidor'])

        print("+-----------+-------------------+--------------------+------------------------+")
        print("| ID: " + show_msg['ID'] + " " * space_id + " | Status: " + show_msg['Status'] + " " * space_status + " | Temperatura: " + show_msg['Temperatura'] + " " * space_temperature + " | Servidor: " + show_msg['Servidor'] + " " * space_server + " |")
        print("+-----------+-------------------+--------------------+------------------------+")

def clear_terminal():
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas (Linux, macOS)
        os.system('clear')
    