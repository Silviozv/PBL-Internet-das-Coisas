import socket
import threading

class Dispositivo:

    def __init__(self):

        self.ip_local = socket.gethostbyname( socket.gethostname())
        self.status = 'desligado'
        self.temperatura = 0

class Conexao:

    def __init__(self):

        self.porta_tcp = 5050
        self.porta_udp = 5060

        self.dispositivo_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.dispositivo_udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

        self.ip_servidor = ""
        self.servidor_conectado = False
        self.lock = threading.Lock()