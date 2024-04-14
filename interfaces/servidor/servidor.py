import threading
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
            storage.connections[address_sender[0]] = connection_sender
        print("Nova conexao:", address_sender)

# Receber os dados enviados por udp (parece que funciona) (retirar os prints depois)
def receive_data_udp():

    while True:

        data, address = connection_server.udp_server.recvfrom(2048)

        if data.decode('utf-8') == "Conexao encerrada":

            if (address[0]) in storage.data_udp_devices:
                
                with connection_server.lock:
                    storage.data_udp_devices.pop(address[0])
            
            with connection_server.lock:
                storage.connections.pop(address[0])
            #print("Lista dados = ", storage.data_udp_devices)
            #print("Lista ips = ", storage.connections)

        else:

            #print(data.decode('utf-8'))
            #print(address[0])
            with connection_server.lock:
                storage.data_udp_devices[address[0]] = eval(data.decode('utf-8'))
            #print("Lista dados = ", storage.data_udp_devices)
            #print("Lista ips = ", storage.connections)

# Envio de comandos para o dispositivo
def send_command(device_ip: str, request: dict):

    storage.connections[device_ip].send(str(request).encode('utf-8'))
    response = eval(storage.connections[device_ip].recv(2048).decode('utf-8'))

    if (response['Tipo de resposta'] == 'Permissão de coleta de dados UDP'):

        if (response['Resposta'] == 'Coleta permitida'):

            response = {'Tipo de resposta': 'Dicionário', 'Resposta': storage.data_udp_devices[device_ip]}
            
        elif (response['Resposta'] == 'Coleta não permitida'):

            response = {'Tipo de resposta': 'Mensagem de resposta', 'Resposta': response['Justificativa']}

    return response

def get_devices_ip():

    return list(storage.connections.keys())
