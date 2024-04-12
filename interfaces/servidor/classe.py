import socket
import threading

class Storage:

    def __init__(self):

        self.connections = {}
        self.data_udp_devices = {}

class Connection_server:

    def __init__(self):

        self.server_ip = socket.gethostbyname( socket.gethostname())

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind( (self.server_ip, self.tcp_port))
        self.tcp_server.listen()

        self.udp_server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind( (self.server_ip, self.udp_port))

        self.lock = threading.Lock()