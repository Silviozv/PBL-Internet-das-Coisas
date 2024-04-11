import socket

class Armazenamento:

    def __init__(self):

        self.conexoes = {}
        self.dados_dispositivos = {}

class Conexao_servidor:

    def __init__(self):

        self.ip_servidor = socket.gethostbyname( socket.gethostname())

        self.porta_tcp = 5050
        self.porta_udp = 5060

        self.servidor_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_tcp.bind( (self.ip_servidor, self.porta_tcp))
        self.servidor_tcp.listen()

        self.servidor_udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor_udp.bind( (self.ip_servidor, self.porta_udp))