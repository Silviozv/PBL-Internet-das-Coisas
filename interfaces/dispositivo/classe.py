import socket
import threading

class Sensor:

    def __init__(self):

        self.local_ip = socket.gethostbyname( socket.gethostname())
        self.description = 'Sensor de temperatura'
        self.status = 'desligado'
        self.temperature = '0 °C'

        self.available_commands = {'1': 'Ligar', '2': 'Desligar', '3': 'Retornar medida de temperatura'}
        self.commands_description = {'1': {'Entrada': '', 'Método HTTP': 'POST'}, '2': {'Entrada': '', 'Método HTTP': 'POST'}, '3': {'Entrada': '', 'Método HTTP': 'GET'}}

    def get_atributes(self) -> str:

        status = self.status.capitalize()
        response = f"IP local: {self.local_ip}\nDescrição: {self.description}\nStatus: {status}\nTemperatura: {self.temperature}"
        return response

    # Dados a serem enviados via UDP
    def get_returning_data(self) -> dict:

        data = {"Temperatura": self.temperature}
        return data
    
    def get_status(self) -> str:

        return self.status
    
    def get_general_description(self) -> dict:

        status = self.status.capitalize()
        general_description = {'Descrição': self.description, 'Status': status} 
        return general_description
    
    def get_available_commands(self) -> dict:

        return self.available_commands
    
    def get_commands_description(self) -> dict:

        return self.commands_description

    def set_temperature(self) -> str:

        try:
            new_temperature = int(input("\nTemperatura: "))

            if -50 < new_temperature < 300:
                self.temperature = (f'{new_temperature} °C')
                return "Medida de temperatura atualizada"
            else:
                raise ValueError
            
        except (ValueError) as e:
            return "Valor inválido"

    def turn_on(self) -> str:

        if self.status == 'desligado':
            with threading.Lock():
                self.status = 'ligado'

            return "Dispositivo ligado"

        else:
            return "Dispositivo já está ligado"
        
    def turn_off(self) -> str:

        if (self.status == 'ligado'):
            with threading.Lock():
                self.status = 'desligado'

            return "Dispositivo desligado"

        else:
            return "Dispositivo já está desligado" 


class Radio:

    def __init__(self):

        self.local_ip = socket.gethostbyname( socket.gethostname())
        self.description = 'Aparelho de som via internet'
        self.type = 'Atuante'
        self.status = 'desligado'
        self.music = 'Nenhuma'

    def get_atributes(self) -> str:

        status = self.status.capitalize()
        response = f"IP local: {self.local_ip}\nDescrição: {self.description}\nStatus: {status}\nMúsica: {self.music}"
        return response
    
    def get_status(self) -> str:

        return self.status
    
    def get_type(self) -> str:

        return self.type
    
    def get_general_description(self) -> dict:

        status = self.status.capitalize()
        general_description = {'Descrição': self.description, 'Status': status, 'Música': self.music} 
        return general_description
    
    def get_available_commands(self) -> list:

        available_commands = ['Ligar', 'Desligar', 'Selecionar música']
        return available_commands
    
    def set_music(self, new_music: str) -> str:

        with threading.Lock():
            self.music = new_music

        return "Dado selecionado"
            
    def turn_on(self) -> str:

        if self.status == 'desligado':
            with threading.Lock():
                self.status = 'ligado'

            return "Dispositivo ligado"

        else:
            return "Dispositivo já está ligado"
        
    def turn_off(self) -> str:

        if (self.status == 'ligado'):
            with threading.Lock():
                self.status = 'desligado'

            return "Dispositivo desligado"

        else:
            return "Dispositivo já está desligado" 

class Connection_device:

    def __init__(self):

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.udp_device = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

        self.server_ip = ""
        self.server_connected = False
        self.lock = threading.Lock()

    def start_connection(self) -> str:

        if (self.server_connected == False):
            server_ip = input("\nIP servidor: ")
            try:
                self.tcp_device.connect( (server_ip, self.tcp_port))

                with self.lock:
                    self.server_ip = server_ip
                    self.server_connected = True

                return "Conexão estabelecida"
                    
            except (ConnectionRefusedError, socket.gaierror, OSError) as e:
                return "Conexão impossibilitada"

        else:
            return "Conexão já estabelecida"

    def end_connection(self) -> str:

        if (self.server_connected == True):

            with self.lock:
                self.server_connected = False
                self.tcp_device.close()
                self.restart_tcp_connection()

            return "Conexão encerrada"

        else:
            return "Não há um servidor conectado"

    def restart_tcp_connection(self):

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)