import threading
import time
from classe import Storage, Connection_server

# lógica embaralhada
# recebe as conexões; armazena os sockets e printa; o comando de resposta é um rascunho

# É para colocar como global?

storage = Storage()
connection_server = Connection_server()
print(connection_server.server_ip)

# Aceitar dispositivos que iniciam conexões (parece que funciona) (é preciso retirar o print depois e a função coletar)
def receive_connection_tcp():
    
    while True:

        connection_sender, address_sender = connection_server.tcp_server.accept()
        with connection_server.lock:
            device_id = calculate_device_id(address_sender[0])
            storage.connections_id[device_id] = address_sender[0]
            storage.connections[address_sender[0]] = connection_sender
            storage.devices_commands_description[address_sender[0]] = eval(storage.connections[address_sender[0]].recv(2048).decode('utf-8'))
            storage.connections[address_sender[0]].send(device_id.encode('utf-8'))
            print(storage.devices_commands_description[address_sender[0]])
        print("Nova conexao:", address_sender)

# Receber os dados enviados por udp (parece que funciona) (retirar os prints depois)
def receive_data_udp():

    while True:

        data, address = connection_server.udp_server.recvfrom(2048)
        with connection_server.lock:
            storage.data_udp_devices[address[0]] = {'Sinalizador de mudança': True, 'Dados': eval(data.decode('utf-8'))}


# Envio de comandos para o dispositivo
def send_command(device_id: str, request: dict):

    device_ip = storage.connections_id[device_id]

    if ( 1 <= int(request['Comando']) <= len(storage.devices_commands_description[device_ip])):

        if ( storage.devices_commands_description[device_ip][request['Comando']]['Coleta de dados UDP'] == False):

            storage.connections[device_ip].send(str(request).encode('utf-8'))
            response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))
            print(1)

        elif ( storage.devices_commands_description[device_ip][request['Comando']]['Coleta de dados UDP'] == True):
            print(5)
            data = get_data_udp( device_ip)
            if ( data == {}):
                response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': 'Não foram retornados dados do dispositivo'}
                print(2)
            elif (data['Válido'] == False):
                response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': data['Justificativa']}
                print(3)
            else:
                data.pop('Válido')
                response = {'Tipo de resposta': 'Dicionário', 'Resposta': data}
                print(4)

    else:

        storage.connections[device_ip].send(str(request).encode('utf-8'))
        response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))
        print(6)

    return response

def validate_communication(): 

    keys = []

    for key in storage.connections_id.keys():
        try:
            device_ip = storage.connections_id[key]

            request = {'Comando': '-1'}
            storage.connections[device_ip].send(str(request).encode('utf-8'))
            storage.connections[device_ip].recv(2048).decode('utf-8')

        except (ConnectionResetError) as e:
            keys.append(key)
            
    for i in range(len(keys)):   
        device_ip = storage.connections_id[keys[i]]
        storage.connections_id.pop(keys[i])
        storage.connections.pop(device_ip)
        storage.devices_commands_description.pop(device_ip)
        if device_ip in storage.data_udp_devices:
            storage.data_udp_devices.pop(device_ip)

def get_devices_id():

    return list(storage.connections_id.keys())

def get_device_commands_description( device_id: str):

    device_ip = storage.connections_id[device_id]

    return storage.devices_commands_description[device_ip]

def get_data_udp( device_ip: str) -> dict:
    
    if ( device_ip in storage.data_udp_devices):

        data = storage.data_udp_devices[device_ip]['Dados']
        begin = time.time()
        storage.data_udp_devices[device_ip]['Sinalizador de mudança'] = False

        while (storage.data_udp_devices[device_ip]['Sinalizador de mudança'] == False and data != {}):

            end = time.time()
            if (end - begin == 1):
                data = {}
            
    else:

        data = {}
            
    return data

def calculate_device_id( device_ip: str) -> str:

    aux_position = device_ip.find('.')

    while (aux_position != -1):
        device_ip = device_ip[(aux_position + 1):]
        aux_position = device_ip.find('.')
    

    id = f"DE{device_ip}"
    
    return id
