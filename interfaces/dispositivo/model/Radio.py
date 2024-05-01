import socket
import threading


class Radio:

    def __init__(self):

        self.local_ip = socket.gethostbyname( socket.gethostname())
        self.description = 'Aparelho de som via internet'
        self.status = 'desligado'
        self.music = '-----'
        self.music_status = '-------'

        self.available_commands = {'1': 'Ligar', '2': 'Desligar', '3': 'Setar música', '4': 'Tocar', '5': 'Pausar'}
        self.commands_description = {'1': {'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, '2': {'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, '3': {'Entrada': 'Música', 'Método HTTP': 'PATCH', 'Coleta de dados UDP': False}, '4': {'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, '5': {'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}}

    def get_query_data(self, server_connected: bool, id: str) -> str:

        status = self.status.capitalize()
        music = self.music.upper()
        if (server_connected == False):
            status_server = 'Desconectado'
        elif (server_connected == True):
            status_server = 'Conectado'
        response = {'ID': id,'Status': status, 'Música atual': music, 'Status da música': self.music_status, 'Servidor': status_server}
        return response
    
    def get_status(self) -> str:

        return self.status
    
    def get_general_description(self) -> dict:

        status = self.status.capitalize()
        general_description = {'Descrição': self.description, 'Status do dispositivo': status, 'Música atual': self.music, 'Status da música': self.music_status} 
        return general_description
    
    def get_available_commands(self) -> list:

        return self.available_commands
    
    def get_commands_description(self) -> dict:

        return self.commands_description

    def set_music(self, new_music: str) -> str:

        with threading.Lock():
            self.music = new_music
            if self.status == 'ligado':
                self.music_status = 'Tocando'
            elif self.status == 'desligado':
                self.music_status = 'Pausada'

        return "Música selecionada"
    
    def play_music(self):

        if (self.music_status == '-------'): 
            return "Nenhuma música foi selecionada"

        else:
            if (self.status == 'ligado'):

                if (self.music_status == 'Tocando'):
                    return "A música já está tocando"
                
                elif (self.music_status == 'Pausada'):
                    with threading.Lock():
                        self.music_status = 'Tocando'
                    return "A música foi colocada para tocar"
                
            elif (self.status == 'desligado'):
                return "Aparelho desligado, não tem como modificar status da música"
            
            
    def pause_music(self):

        if (self.music_status == '-------'): 
            return "Nenhuma música foi selecionada"

        else:
            if (self.status == 'ligado'):

                if (self.music_status == 'Tocando'):
                    with threading.Lock():
                        self.music_status = 'Pausada'
                    return "A música foi pausada"
                
                elif (self.music_status == 'Pausada'):
                    return "A música já está pausada"
                
            elif (self.status == 'desligado'):
                return "Aparelho desligado, não tem como modificar status da música"   

    def turn_on(self) -> str:

        if self.status == 'desligado':
            with threading.Lock():
                self.status = 'ligado'
                if ( self.music != '-----'):
                    self.music_status = 'Tocando'

            return "Dispositivo ligado"

        else:
            return "Dispositivo já está ligado"
        
    def turn_off(self) -> str:

        if (self.status == 'ligado'):
            with threading.Lock():
                self.status = 'desligado'
                if ( self.music != '-----'):
                    self.music_status = 'Pausada'

            return "Dispositivo desligado"

        else:
            return "Dispositivo já está desligado" 
