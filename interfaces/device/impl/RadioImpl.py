""" 
Módulo contendo as funções de implementação do Radio, incluindo: o menu 
de requisições do usuário e o 'looping' de recebimento das requisições do servidor.
"""

import socket
import os
import threading


def menu( radio, connection):
    """
    Menu de opções do dispositivo. São exibidas as opções do menu, e as resposta das 
    requisições do usuário logo abaixo. Ocorre a atualização da tela a cada requisição. 

    :param radio: Objeto que representa o radio.
    :type radio: object
    :param connection: Objeto que representa a conexão do dispositivo com o servidor.
    :type connection: object
    """

    show_msg = 'Sistema iniciado'

    while True:
 
        show_scream(show_msg)
        option = input("\n  > ").strip()

        # Respostas para os casos em desenvolvimento
        if (option == '1'):
            show_msg = connection.start_connection(radio.get_commands_description())

        elif (option == '2'):
            show_msg = connection.end_connection()

        elif (option == '3'):
            show_msg = radio.turn_on()
        
        elif (option == '4'):       
            show_msg = radio.turn_off()
            
        elif (option == '5'):
            show_msg = radio.get_query_data(connection.server_status, connection.device_id)
         
        elif (option == '6'):
            music = input("\n  Música: ")
            show_msg = radio.set_music(music)

        elif (option == '7'):
            show_msg = radio.play_music()

        elif (option == '8'):
            show_msg = radio.pause_music()    

        else:
            show_msg = 'Opção inválida'

        clear_terminal()


def server_request_tcp( radio, connection):
    """
    Recebimento das requisições do servidor e envio das resposta de retorno. Se o 
    servidor estiver conectado, é esperada a requisição, depois, é verificado se o 
    comando recebido é válido ou não. Descrição do protocolo:

    0: Envio periódico para confirmar a conexão;
    1: Ligar dispositivo;
    2: Desligar dispositivo;
    3: Setar música;
    4: Colocar música para tocar;
    5: Pausar música;
    6: Envio da descrição geral do dispositivo.

    Se o comando 0 não for recebido no tempo indicado, ou a conexão for encerrada, é 
    iniciado o 'looping' de reconexão em outra thread.

    :param radio: Objeto que representa o radio.
    :type radio: object
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

                if ( not (-1 < request['Comando'] <= len(radio.get_commands_description()) + 1)):
                    raise ValueError

                # Opções de respostas de comandos em desenvolvimento
                if (request['Comando'] == 0):
                    response = 'Recebido'
                    connection.tcp_device.send(response.encode('utf-8'))

                elif (request['Comando'] == 1):
                    response_message = radio.turn_on()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 2):
                    response_message = radio.turn_off()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 3):
                    response_message = radio.set_music(request['Entrada'])
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 4):
                    response_message = radio.play_music()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 5):
                    response_message = radio.pause_music()
                    response = {'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))    

                elif (request['Comando'] == 6):
                    general_description = radio.get_general_description()
                    response = {'Resposta': general_description}
                    connection.tcp_device.send(str(response).encode('utf-8'))

            except (ValueError) as e:
                response = {'Resposta': 'Comando inválido'}
                connection.tcp_device.send(str(response).encode('utf-8'))

            except (ConnectionAbortedError, ConnectionResetError, OSError, socket.timeout) as e:   # Quando o dispositivo cancela a comunicação
                if connection.server_ip != "":
                    connection.server_status = 'Reconectando'
                    threading.Thread(target=connection.loop_reconnection, args=[ radio.get_commands_description()]).start()


def show_scream( show_msg):
    """
    Exibição da tela do dispositivo ao usuário. 

    :param show_msg: Texto que deve ser exibido abaixo das requisições, podendo ser uma 
    string ou um dicionário.
    """

    print("\n+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
    print("|                        APARELHO DE SOM VIA INTERNET                         |")
    print("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

    print('''+-----------------------------------------------------------------------------+
|                                                                             |
|                      [ 1 ]    CONECTAR AO SERVIDOR                          |
|                      [ 2 ]    DESCONECTAR DO SERVIDOR                       |
|                      [ 3 ]    LIGAR                                         |
|                      [ 4 ]    DESLIGAR                                      |
|                      [ 5 ]    CONSULTAR DADOS                               |
|                      [ 6 ]    SETAR MÚSICA                                  |
|                      [ 7 ]    TOCAR                                         |
|                      [ 8 ]    PAUSAR                                        |
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
        space_id = 9 - len(show_msg['ID'])
        space_status = 13 - len(show_msg['Status'])
        space_server = 16 - len(show_msg['Servidor'])

        print("+------------------+--------------------------+-------------------------------+")
        print("|    ID: " + show_msg['ID'] + " " * space_id + " |    Status: " + show_msg['Status'] + " " * space_status + " |    Servidor: " + show_msg['Servidor'] + " " * space_server + " |")
        print("+------------------+--------------------------+-------------------------------+")
       
        if ( show_msg['Música atual'] != '-----'):

            space_before_music = (75 - len(show_msg['Música atual'])) // 2
            space_after_music = 75 - (space_before_music + len(show_msg['Música atual']))

            print("| " + " " * space_before_music + show_msg['Música atual'] + " " * space_after_music + " |")
            print("|" + " " * 35 + show_msg['Status da música'] + " " * 35 + "|")
            print("+-----------------------------------------------------------------------------+")


def clear_terminal():
    """
    Limpa os dados da tela de exibição do usuário, adaptando-se ao sistema operacional atual. 
    """
    
    if os.name == 'nt':  
        os.system('cls')
    else: 
        os.system('clear')
