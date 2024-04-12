import socket
import threading

class Sensor:

    def __init__(self):

        self.local_ip = socket.gethostbyname( socket.gethostname())
        self.description = 'Sensor de temperatura'
        self.status = 'desligado'
        self.temperature = 0

    # Dados a serem enviados via UDP
    def get_returning_data(self) -> dict:

        informacoes = {"Temperatura": self.temperature}
        return informacoes
    
    def get_status(self) -> str:

        return self.status

class Connection_device:

    def __init__(self):

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.udp_device = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

        self.server_ip = ""
        self.server_connected = False
        self.lock = threading.Lock()

    def restart_tcp_connection(self):

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)