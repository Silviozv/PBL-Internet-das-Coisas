import os
import threading  
from classe import Radio, Connection_device

radio = Radio()
connection = Connection_device()

# Menu de opções diretas para o dispositivo (parece que as opções funcionam bem, incluindo a conexão e desconexão)
def menu():

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
            show_msg = radio.get_query_data(connection.server_connected, connection.device_id)
         
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

def show_scream( show_msg):

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
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas (Linux, macOS)
        os.system('clear')

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp).start()
    menu()

if __name__=="__main__":
    iniciar()