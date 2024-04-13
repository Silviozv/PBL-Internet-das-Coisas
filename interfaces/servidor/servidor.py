import threading
from classe import Storage, Connection_server

# lógica embaralhada
# recebe as conexões; armazena os sockets e printa; o comando de resposta é um rascunho

# É para colocar como global?

storage = Storage()
connection_server = Connection_server()
print(connection_server.server_ip)

# Funcção de teste de requisições
def enviar_comando():

    while True:
        ip_device = input("\nIP dispositivo: ")
        comando = int(input("Comando: "))

        if comando == 1:
            print(get_available_commands(ip_device))
        elif comando == 2:
            print(get_general_description(ip_device))
        elif comando == 3:
            print(turn_on_device(ip_device))
        elif comando == 4:
            print(turn_off_device(ip_device))
        elif comando == 5:
            musica = input("Música: ")

            print(get_data_udp(ip_device))

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
                storage.data_udp_devices[address[0]] = data.decode('utf-8')
            #print("Lista dados = ", storage.data_udp_devices)
            #print("Lista ips = ", storage.connections)

# Comando de retorno dos comandos disponíveis
def get_available_commands(device_ip: str) -> str:

    storage.connections[device_ip].send("1".encode('utf-8')) 
    available_commands = storage.connections[device_ip].recv(2048).decode('utf-8')
    return eval(available_commands)

# Comando de retorno da descrição geral do dipositivo
def get_general_description(device_ip: str) -> str:

    storage.connections[device_ip].send("2".encode('utf-8')) 
    general_description = storage.connections[device_ip].recv(2048).decode('utf-8')
    return eval(general_description)

def turn_on_device( device_ip: str) -> str:

    storage.connections[device_ip].send("3".encode('utf-8')) 
    response = storage.connections[device_ip].recv(2048).decode('utf-8')
    return response

def turn_off_device( device_ip: str) -> str:

    storage.connections[device_ip].send("4".encode('utf-8')) 
    response = storage.connections[device_ip].recv(2048).decode('utf-8')
    return response

# Comando de retorno do dado UDP
# Coletar o dado retornado via UDP (parece que funciona mas tem que funcionar com a api)
def get_data_udp( device_ip: str) -> str:

    storage.connections[device_ip].send("5".encode('utf-8')) 
    status = storage.connections[device_ip].recv(2048).decode('utf-8')

    if ( status == 'ligado'):
      
        return eval(storage.data_udp_devices[device_ip])
    
    elif ( status == 'desligado'):

        return "Dispositivo desligado, não é possível coletar dados de leitura"

def set_data( device_ip: str, data: str) -> str:

    storage.connections[device_ip].send((f"5 {data}").encode('utf-8')) 
    response = storage.connections[device_ip].recv(2048).decode('utf-8')
    return response
   
def get_device_type( device_ip: str) -> str:

    storage.connections[device_ip].send("6".encode('utf-8')) 
    type = storage.connections[device_ip].recv(2048).decode('utf-8')
    return {"Tipo": type}

def get_devices_ip():

    return list(storage.connections.keys())

def iniciar():

    threading.Thread(target=receive_connection_tcp).start()
    threading.Thread(target=receive_data_udp).start()
    enviar_comando()

#iniciar()