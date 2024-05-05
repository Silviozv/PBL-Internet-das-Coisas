""" 
Módulo contendo as funções de implementação do sensor de temperatura, incluindo: o menu 
de requisições do usuário, o 'looping' de recebimento das requisições do servidor, e 
o envio periódico dos dados armazenados na medida de temperatura.
"""

import socket
import os
import time
import threading


def menu( sensor: object, connection: object):
    """
    Menu de opções do dispositivo. São exibidas as opções do menu, e as resposta das 
    requisições do usuário logo abaixo. Ocorre a atualização da tela a cada requisição. 

    :param sensor: Objeto que representa o sensor de temperatura.
    :type sensor: object
    :param connection: Objeto que representa a conexão do dispositivo com o servidor.
    :type connection: object
    """

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


def server_request_tcp( sensor, connection):
    """
    Recebimento das requisições do servidor e envio das resposta de retorno. Se o 
    servidor estiver conectado, é esperada a requisição, depois, é verificado se o 
    comando recebido é válido ou não. Descrição do protocolo:

    0: Envio periódico para confirmar a conexão;
    1: Ligar dispositivo;
    2: Desligar dispositivo;
    3: Enviar medida de temperatura, porém, como esse dado é enviado periodicamente por 
       comunicação UDP, esse comando não é recebido, estando destacado só como representação;
    4: Envio da descrição geral do dispositivo;
    5: Envio dos comandos disponíveis ao usuário.

    Se o comando 0 não for recebido no tempo indicado, ou a conexão for encerrada, é 
    iniciado o 'looping' de reconexão paralelamente.

    :param sensor: Objeto que representa o sensor de temperatura.
    :type sensor: object
    :param connection: Objeto que representa a conexão do dispositivo com o servidor.
    :type connection: object
    """

    while True:

        if (connection.server_status == 'Conectado'):

            try:

                request = connection.tcp_device.recv(2048).decode('utf-8')

                if (request == ""):
                    raise ConnectionResetError
                
                request = eval(request)

                request['Comando'] = int(request['Comando'])

                if ( not (-1 < request['Comando'] <= len(sensor.get_commands_description()) + 1)):
                    raise ValueError

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

            except (ValueError) as e:
                response = {'Resposta': 'Comando inválido'}
                connection.tcp_device.send(str(response).encode('utf-8'))

            except (ConnectionAbortedError, ConnectionResetError, OSError, socket.timeout) as e:  
                if connection.server_ip != "":
                    connection.server_status = 'Reconectando'
                    threading.Thread(target=connection.loop_reconnection, args=[ sensor.get_commands_description()]).start()


def send_data_udp( sensor, connection):    
    """
    'Looping' de envio dos dados periódicos via comunicação UDP. Os dados só são enviados 
    se o servidor estiver conectado e alguma medida de temperatura esteja setada. Dependendo 
    do status do dispositivo, os dados enviados podem ser válidos ou não.

    :param sensor: Objeto que representa o sensor de temperatura.
    :type sensor: object
    :param connection: Objeto que representa a conexão do dispositivo com o servidor.
    :type connection: object
    """

    while True:
            
        if (connection.server_status == "Conectado" and sensor.temperature != "-----"):
            
            try:
                if (sensor.status == 'ligado'):
                    data = sensor.get_returning_data()
                    data['Válido'] = True
                elif (sensor.status == 'desligado'):
                    data = {}
                    data['Válido'] = False
                    data['Justificativa'] = 'Dispositivo desligado, não é possível coletar os dados'
                connection.udp_device.sendto( str(data).encode('utf-8'), (connection.server_ip, connection.udp_port))

            except (OSError, socket.timeout) as e:
                pass

        time.sleep(0.8)


def show_scream( show_msg):
    """
    Exibição da tela do dispositivo ao usuário. 

    :param show_msg: Texto que deve ser exibido abaixo das requisições, podendo ser uma 
    string ou um dicionário.
    """

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
    """
    Limpa os dados da tela de exibição do usuário, adaptando-se ao sistema operacional atual. 
    """

    if os.name == 'nt':  
        os.system('cls')
    else: 
        os.system('clear')
    