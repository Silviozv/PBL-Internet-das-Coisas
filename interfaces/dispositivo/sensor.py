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

                request = eval(connection.tcp_device.recv(2048).decode('utf-8'))
                request['Comando'] = int(request['Comando'])

                # Opções de respostas de comandos em desenvolvimento
                if (request['Comando'] == 0):

                    if ( not (-1 < request['Comando'] <= len(sensor.get_available_commands()) + 2)):
                        raise ValueError
     
                    commands_description = sensor.get_commands_description()
                    response = {'Tipo de resposta': 'Dicionário', 'Resposta': commands_description}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 1):

                    response_message = sensor.turn_on()
                    response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 2):

                    response_message = sensor.turn_off()
                    response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': response_message}
                    connection.tcp_device.send(str(response).encode('utf-8'))

                elif (request['Comando'] == 3):
                    
                    status = sensor.get_status()

                    if (status == 'ligado'):

                        response = {'Tipo de resposta': 'Permissão de coleta de dados UDP', 'Resposta': 'Coleta permitida', 'Justificativa': ''}

                    elif (status == 'desligado'):

                        response = {'Tipo de resposta': 'Permissão de coleta de dados UDP', 'Resposta': 'Coleta não permitida', 'Justificativa': 'Dispositivo desligado, não é possível coletar os dados'}

                    connection.tcp_device.send(str(response).encode('utf-8'))

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

            except (ConnectionAbortedError) as e:
                pass

# Enviar os dados via UDP (parece que ta funcionando)
def send_data_udp():    

    while True:
            
        if (connection.server_ip != "" and sensor.status == 'ligado'):
            data = sensor.get_returning_data()
            connection.udp_device.sendto( str(data).encode('utf-8'), (connection.server_ip, connection.udp_port))

def iniciar():

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp).start()
    threading.Thread(target=send_data_udp).start()
    menu()

if __name__=="__main__":
    iniciar()
