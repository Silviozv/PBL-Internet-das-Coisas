import threading
import time
import socket
from classe import Storage, Connection_server

storage = Storage()
connection_server = Connection_server()

# Aceitar dispositivos que iniciam conexões (parece que funciona) (é preciso retirar o print depois e a função coletar)
def receive_connection_tcp():
    
    print("\nServidor iniciando...")
    print("IP do servidor:", connection_server.server_ip)
    print()

    while True:

        connection_sender, address_sender = connection_server.tcp_server.accept()
        threading.Thread( target=dealing_connection_tcp, args=[ connection_sender, address_sender[0]]).start()

def dealing_connection_tcp( connection_sender: object, address_sender: str):

    response = connection_sender.recv(2048).decode('utf-8')

    if (response == "Checagem"):

        if (address_sender in storage.connections):
            connection_sender.send("Conectado".encode('utf-8'))
        else:
            connection_sender.send("Desconectado".encode('utf-8'))

    elif (response == "Conexão"):

        with connection_server.lock:
            connection_sender.settimeout(3)
            device_id = calculate_device_id(address_sender)
            storage.connections_id[device_id] = address_sender
            storage.connections[address_sender] = connection_sender
            storage.devices_commands_description[address_sender] = eval(storage.connections[address_sender].recv(2048).decode('utf-8'))
            storage.connections[address_sender].send(device_id.encode('utf-8'))

        print("Nova conexao:", address_sender)
    
# Receber os dados enviados por udp (parece que funciona) (retirar os prints depois)
def receive_data_udp():

    while True:

        data, address = connection_server.udp_server.recvfrom(2048)
        if (address[0] in storage.connections):
            with connection_server.lock:
                storage.data_udp_devices[address[0]] = {'Sinalizador de mudança': True, 'Dados': eval(data.decode('utf-8'))}


# Envio de comandos para o dispositivo
def send_command(device_id: str, request: dict):

    device_ip = storage.connections_id[device_id]

    if ( 1 <= int(request['Comando']) <= len(storage.devices_commands_description[device_ip])):

        if ( storage.devices_commands_description[device_ip][request['Comando']]['Coleta de dados UDP'] == False):
            
            storage.connections[device_ip].send(str(request).encode('utf-8'))
            response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))

        elif ( storage.devices_commands_description[device_ip][request['Comando']]['Coleta de dados UDP'] == True):
            
            data = get_data_udp( device_ip)
            if ( data == {}):
                response = {'Resposta': 'Não foram retornados dados do dispositivo'}
            elif (data['Válido'] == False):
                response = {'Resposta': data['Justificativa']}
            else:
                data.pop('Válido')
                response = {'Resposta': data}

    else:

        storage.connections[device_ip].send(str(request).encode('utf-8'))
        response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))

    return response


def validate_communication( device_id: str) -> bool: 

    connected = True

    try:
        device_ip = storage.connections_id[device_id]

        request = {'Comando': '0'}
        storage.connections[device_ip].send(str(request).encode('utf-8'))
        storage.connections[device_ip].recv(2048).decode('utf-8')

    except (ConnectionResetError, ConnectionAbortedError, socket.timeout) as e:
        connected = False
            
    if (connected == False):  
        device_ip = storage.connections_id[device_id]
        storage.connections_id.pop(device_id)
        storage.connections[device_ip].close()
        storage.connections.pop(device_ip)
        storage.devices_commands_description.pop(device_ip)
        if device_ip in storage.data_udp_devices:
            storage.data_udp_devices.pop(device_ip)

    return connected


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