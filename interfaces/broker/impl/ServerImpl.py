""" 
Módulo contendo as funções de implementação do Servidor Broker. Incluindo: 
recebimento de conexões de comunicação TCP e dados de comunicação UDP; 
validação de conexões; envio de comandos de requisição; e coleta de dados.
"""

import threading
import time
import socket
from model.Storage import Storage
from model.Connection_server import Connection_server


"""
Inicializando objetos base para a implementação do Servidor Broker.
"""
storage = Storage()
connection_server = Connection_server()


def receive_connection_tcp():
    """
    Recebimento de pedidos de conexão TCP. Quando um pedido de conexão é detectado, 
    é criada uma 'thread' para fazer o processo inicial de confirmar a conexão.
    """

    print("\nServidor Broker iniciando...")
    print("IP do servidor:", connection_server.server_ip)
    print()

    while True:
        connection_sender, address_sender = connection_server.tcp_server.accept()
        threading.Thread( target=dealing_connection_tcp, args=[ connection_sender, address_sender[0]]).start()


def dealing_connection_tcp( connection_sender: object, address_sender: str):
    """
    Faz o processo inicial para confirmar uma nova conexão. É identificado se a 
    conexão iniciada tem o intuito de checar se o Servidor Broker está conectado 
    ao dispositivo ou não, retornando essa informação ao dispositivo. Caso seja 
    uma conexão para construir uma comunicação sólida entre os dois, é feito o 
    processo de enviar e receber as informações necessários. O dispositivo envia 
    a descrição dos seus comandos, e o Servidor Broker envia o ID calculado. Após 
    o processo de consolidar a comunicação, é chamada a função de enviar comandos 
    de confirmação periódicos ao dispositivo.

    :param connection_sender: Objeto que representa a comunicação TCP com o dispositivo.
    :type connection_sender: object
    :param address_sender: Endereço IP do dispositivo.
    :type address_sender: str
    """

    response = connection_sender.recv(2048).decode('utf-8')

    if (response == "Checagem"):

        if (address_sender in storage.connections):
            connection_sender.send("Conectado".encode('utf-8'))
        else:
            connection_sender.send("Desconectado".encode('utf-8'))

    elif (response == "Conexão"):

        with connection_server.lock:
            connection_sender.settimeout(5)
            device_id = calculate_device_id(address_sender)
            storage.connections_id[device_id] = address_sender
            storage.connections[address_sender] = connection_sender
            storage.connections[address_sender].send(device_id.encode('utf-8'))
            storage.devices_commands_description[address_sender] = eval(storage.connections[address_sender].recv(2048).decode('utf-8'))
            storage.flags_devices[address_sender] = 0

        print("Nova conexão registrada:", address_sender)
        time.sleep(2)
        loop_validate_communication(device_id)
    

def loop_validate_communication( device_id: str):
    """
    Envia comandos de verificação periódicos ao dispositivo. No 
    intuito de manter a checagem da validade do canal de comunicação. 
    A 'flag' do dispositivo é usada para evitar o uso desse canal de 
    comunicação TCP paralelamente entre processos, evitando condições 
    de corrida. É feita a tentativa de envio a cada 3 segundos.

    :param device_id: ID do dispositivo.
    :type device_id: str
    """

    device_ip  = storage.connections_id[device_id]

    while (device_ip in storage.connections):
        
        try:
            while storage.flags_devices[device_ip] == 1:
                pass

            with connection_server.lock:
                storage.flags_devices[device_ip] = 1

            request = {'Comando': '0'}
            with connection_server.lock:
                storage.connections[device_ip].send(str(request).encode('utf-8'))
                storage.connections[device_ip].recv(2048).decode('utf-8')

        except (ConnectionResetError, ConnectionAbortedError, socket.timeout, BrokenPipeError) as e:
            with connection_server.lock:
                storage.connections_id.pop(device_id)
                storage.connections[device_ip].close()
                storage.connections.pop(device_ip)
                storage.devices_commands_description.pop(device_ip)
                storage.flags_devices.pop(device_ip)
                if device_ip in storage.data_udp_devices:
                    storage.data_udp_devices.pop(device_ip)

        except (KeyError) as e:
            pass
        
        if device_ip in storage.flags_devices:
            with connection_server.lock:     
                storage.flags_devices[device_ip] = 0

        time.sleep(3)


def receive_data_udp():
    """
    Recebe dados pelo canal de comunicação UDP. É checado se o dispositivo 
    está registrado no servidor antes de receber os dados. Se estiver, 
    os dados são armazenados e é setado o sinalizador de mudança daquele 
    dado. Esse sinalizador é usado na função de coleta de dados por canal 
    de comunicação UDP, para saber se a informação chegou em um intervalo 
    de tempo.
    """

    while True:

        data, address = connection_server.udp_server.recvfrom(2048)
        if (address[0] in storage.connections):
            with connection_server.lock:
                storage.data_udp_devices[address[0]] = {'Sinalizador de mudança': True, 'Dados': eval(data.decode('utf-8'))}


def send_command(device_id: str, request: dict) -> dict:
    """
    Envia uma requisição ao dispositivo. É checado pela 'flag' se o objeto de 
    comunicação TCP do dispositivo está sendo usado em outro processo, se 
    estiver, espera ser liberado. Utiliza-se a descrição armazenada dos 
    comandos do dispositivo para saber se é necessário fazer uma coleta dos 
    dados via comunicação UDP, ou envia uma requisição ao dispositivo. 
    A resposta é coletada e é retornada.

    :param device_id: ID do dispositivo.
    :type device_id: str
    :param request: Requisição para o dispositivo.
    :type request: dict
    :return: Resposta da requisição.
    :rtype: dict
    """

    device_ip = storage.connections_id[device_id]

    while storage.flags_devices[device_ip] == 1:
        pass
    
    with connection_server.lock:
        storage.flags_devices[device_ip] = 1

    if ( 1 <= int(request['Comando']) <= len(storage.devices_commands_description[device_ip])):

        if ( storage.devices_commands_description[device_ip][request['Comando']]['Coleta de dados UDP'] == False):
            with connection_server.lock:
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
        with connection_server.lock:
            storage.connections[device_ip].send(str(request).encode('utf-8'))
            response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))

    with connection_server.lock:
        storage.flags_devices[device_ip] = 0

    return response


def validate_communication( device_id: str) -> bool: 
    """
    Checa se o Servidor Broker tem uma comunicação válida com o 
    dispositivo ou não. Antes de usar o objeto de comunicação TCP, é 
    verificada a 'flag' de controle do dispositivo para evitar condições 
    de corrida. É enviado o comando de verificação, se a comunicação for 
    inválida, os dados armazenados do dispositivo são apagados. 

    :param device_id: ID do dispositivo.
    :type device_id: str
    :return: Informação se o dispositivo está conectado ou não.
    :rtype: bool
    """

    if device_id in storage.connections_id:
        device_ip = storage.connections_id[device_id]

        while storage.flags_devices[device_ip] == 1:
                pass

        with connection_server.lock:
            storage.flags_devices[device_ip] = 1

        if device_id in storage.connections_id:

            connected = True

            try:
                request = {'Comando': '0'}
                with connection_server.lock:
                    storage.connections[device_ip].send(str(request).encode('utf-8'))
                    storage.connections[device_ip].recv(2048).decode('utf-8')

            except (ConnectionResetError, ConnectionAbortedError, socket.timeout, BrokenPipeError) as e:
                connected = False
                    
            if (connected == False):  
                with connection_server.lock:
                    storage.connections_id.pop(device_id)
                    storage.connections[device_ip].close()
                    storage.connections.pop(device_ip)
                    storage.devices_commands_description.pop(device_ip)
                    storage.flags_devices.pop(device_ip)

                    if device_ip in storage.data_udp_devices:
                        storage.data_udp_devices.pop(device_ip)

            if device_ip in storage.flags_devices:
                with connection_server.lock:
                    storage.flags_devices[device_ip] = 0

        else:
            connected = False

    else:
        connected = False

    return connected


def get_devices_id():
    """
    Retorna os IDs de todos os dispositivos registrados. 

    :return: IDs registrados atualmente.
    :rtype: list
    """

    return list(storage.connections_id.keys())


def get_device_commands_description( device_id: str):
    """
    Retorna as descrições dos comandos de determinado dispositivo. 
    Identificado a partir do ID.

    :param device_id: ID do dispositivo.
    :type device_id: str
    :return: Descrições dos comandos do dispositivo.
    :rtype: dict
    """

    device_ip = storage.connections_id[device_id]
    return storage.devices_commands_description[device_ip]


def get_data_udp( device_ip: str) -> dict:
    """
    Retorna os dados coletados pelo canal de comunicação UDP. Foi 
    setado um intervalo de tempo de 2 segundo para o dado ser enviado 
    pelo dispositivo. Se não for detectado o recebimento, significa que 
    o dispositivo não está enviando dados. Se for recebido, é retornado.

    :param device_ip: IP do dispositivo.
    :type device_ip: str
    :return: Dados recebidos via canal de comunicação UDP.
    :rtype: dict
    """

    if ( device_ip in storage.data_udp_devices):

        data = storage.data_udp_devices[device_ip]['Dados']
        begin = time.time()
        storage.data_udp_devices[device_ip]['Sinalizador de mudança'] = False

        while (storage.data_udp_devices[device_ip]['Sinalizador de mudança'] == False and data != {}):
            end = time.time()
            if (end - begin == 2):
                data = {}
            
    else:
        data = {}
            
    return data


def calculate_device_id( device_ip: str) -> str:
    """
    Calcula o ID do dispositivo a partir do seu endereço IP.

    :param device_ip: IP do dispositivo.
    :type device_ip: str
    :return: ID do dispositivo.
    :rtype: str
    """

    aux_position = device_ip.find('.')

    while (aux_position != -1):
        device_ip = device_ip[(aux_position + 1):]
        aux_position = device_ip.find('.')

    id = f"DE{device_ip}"
    return id
