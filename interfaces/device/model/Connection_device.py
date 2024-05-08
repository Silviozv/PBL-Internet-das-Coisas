"""
Módulo contendo a classe que representa a conexão de um dispositivo.
"""

import socket
import threading
import time


class Connection_device:
    """ Classe que representa a conexão de um dispositivo. """


    def __init__(self):
        """
        Inicialização dos atributos base da conexão do dispositivo. Incluindo: o ID, as portas de 
        conexão para cada tido de conexão, os objetos socket da conexão e dados relacionados ao 
        servidor.
        """

        self.device_id = "-----"

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.udp_device = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

        self.server_ip = ""
        self.server_status = 'Desconectado'
        self.lock = threading.Lock()


    def start_connection(self, commands_description: dict) -> str:
        """
        Pede o IP do servidor para fazer o processo de iniciar a conexão, caso não tenha nenhum servidor 
        conectado. Depois de mandar o sinal indicando que uma conexão está tentando ser iniciada, são 
        enviadas as descrições dos comandos para serem armazenadas no servidor, em seguida, é recebido o 
        ID calculado pelo servidor. Os atributos da armazenamento dos dados do servidor são modificados. 
        Dependendo do resultado da ação e do status atual da conexão com o servidor, a mensagem de resposta 
        é modificada.

        :param commands_description: Descrição dos comandos disponíveis para requisição.
        :type commands_description: dict
        :return: Resultado da tentativa de início da conexão com o servidor.
        :rtype: str
        """

        if self.server_status == 'Desconectado':
            server_ip = input("\n  IP servidor: ").strip()
            try:
                self.tcp_device.settimeout(5)
                self.tcp_device.connect( (server_ip, self.tcp_port))
                self.tcp_device.send("Conexão".encode('utf-8'))
                self.device_id = self.tcp_device.recv(2048).decode('utf-8')
                self.tcp_device.send(str(commands_description).encode('utf-8'))

                with self.lock:
                    self.server_ip = server_ip
                    self.server_status = 'Conectado'

                return "Conexão estabelecida"
                    
            except (ConnectionRefusedError, socket.gaierror, socket.timeout, OSError) as e:
                return "Conexão impossibilitada"

        elif self.server_status == 'Conectado':
            return "Conexão já estabelecida"
        
        elif self.server_status == 'Reconectando':
            return "Tentando reconectar com o servidor atual..."
        

    def end_connection(self) -> str:
        """
        Encerra a conexão com o servidor atual, caso tenha algum IP de servidor setado. Os 
        objetos da conexão são tratados para encerrar a conexão e os atributos de dados do 
        servidor são atualizados.

        :return: Resultado da tentativa de encerrar a conexão com o servidor.
        :rtype: str
        """

        if self.server_status == 'Conectado' or self.server_status == 'Reconectando':

            with self.lock:
                self.server_status = 'Desconectado'
                self.server_ip = ""
                self.device_id = "-----"
                self.tcp_device.close()
                self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

            return "Conexão encerrada"

        else:
            return "Não há um servidor conectado"
        

    def loop_reconnection(self, commands_description: dict):
        """
        'Loop' para tentar se reconectar com o servidor atual. É enviada uma mensagem de 
        checagem para o servidor, e é esperada a resposta indicando se ele manteve o 
        dispositivo armazenado ou não. Se for recebido que o servidor encerrou a conexão 
        com o dispositivo, é feita uma nova tentativa de recomeçar a conexão. O 'loop' continua 
        até que a reconexão seja feita, ou que seja recebida a confirmação que a conexão 
        ainda é válida.

        :param commands_description: Descrição dos comandos disponíveis para requisição.
        :type commands_description: dict
        """

        while self.server_status == 'Reconectando':

            try:
                tcp_device_check = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                tcp_device_check.settimeout(5)
                tcp_device_check.connect( (self.server_ip, self.tcp_port))
                tcp_device_check.send("Checagem".encode('utf-8'))
                response = tcp_device_check.recv(2048).decode('utf-8')

                if response == "Desconectado":
                    self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                    self.tcp_device.settimeout(5)
                    self.tcp_device.connect( (self.server_ip, self.tcp_port))
                    self.tcp_device.send("Conexão".encode('utf-8'))
                    self.device_id = self.tcp_device.recv(2048).decode('utf-8')
                    self.tcp_device.send(str(commands_description).encode('utf-8'))

                    with self.lock:
                        self.server_status = 'Conectado'

                elif response == "Conectado":
                    with self.lock:
                        self.server_status = 'Conectado'
                        
            except (ConnectionRefusedError, socket.gaierror, socket.timeout, OSError) as e:
                time.sleep(2)
