"""
Módulo contendo a classe que representa os dados de conexão do servidor.
"""

import socket
import threading


class Connection_server:
    """ Classe que representa os dados de conexão do servidor. """

    def __init__(self):
        """
        Inicialização dos atributos base de conexão do servidor. Incluindo: 
        o objeto de comunicação TCP para aceitar conexões; o objeto de comunicação 
        UDP para recebimento de dados; as portas indicadas para comunicação TCP e UDP; 
        e o objeto 'lock' utilizado evitar condições de corrida.
        """

        self.server_ip = socket.gethostbyname( socket.gethostname())

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind( (self.server_ip, self.tcp_port))
        self.tcp_server.listen()

        self.udp_server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind( (self.server_ip, self.udp_port))

        self.lock = threading.Lock()
