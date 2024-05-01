import socket
import threading

class Connection_device:

    def __init__(self):

        self.device_id = "-----"

        self.tcp_port = 5050
        self.udp_port = 5060

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.udp_device = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

        self.server_ip = ""
        self.server_connected = False
        self.lock = threading.Lock()

    def start_connection(self, commands_description: dict) -> str:

        if (self.server_connected == False):
            server_ip = input("\n  IP servidor: ").strip()
            try:
                self.tcp_device.settimeout(5)
                self.tcp_device.connect( (server_ip, self.tcp_port))
                self.tcp_device.send("Conexão".encode('utf-8'))
                self.tcp_device.send(str(commands_description).encode('utf-8'))
                self.device_id = self.tcp_device.recv(2048).decode('utf-8')
                self.tcp_device.settimeout(None)

                with self.lock:
                    self.server_ip = server_ip
                    self.server_connected = True

                return "Conexão estabelecida"
                    
            except (ConnectionRefusedError, socket.gaierror, socket.timeout, OSError) as e:
                return "Conexão impossibilitada"

        else:
            return "Conexão já estabelecida"

    def end_connection(self) -> str:

        if (self.server_connected == True):

            with self.lock:
                self.server_connected = False
                self.server_ip = ""
                self.device_id = "-----"
                self.tcp_device.close()
                self.restart_tcp_obj()

            return "Conexão encerrada"

        else:
            return "Não há um servidor conectado"

    def restart_tcp_obj(self):

        self.tcp_device = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

    def check_connection(self):

        if (self.server_connected == True):

            try:
                tcp_device_check = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                tcp_device_check.settimeout(5)
                tcp_device_check.connect( (self.server_ip, self.tcp_port))
                tcp_device_check.send("Checagem".encode('utf-8'))
                response = tcp_device_check.recv(2048).decode('utf-8')
                if (response == "Desconectado"):
                    self.end_connection()
            except (ConnectionRefusedError, socket.gaierror, socket.timeout, OSError) as e:
                self.end_connection()
