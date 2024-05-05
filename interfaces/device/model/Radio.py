"""
Módulo contendo a classe do Radio.
"""

import socket
import threading


class Radio:
    """ Classe que representa um Radio. """


    def __init__(self):
        """
        Inicialização dos atributos base do Radio. Incluindo: a descrição, o status, os dados da 
        música atual, os comandos disponíveis para o usuário e as suas descrições.
        """

        self.description = 'Aparelho de som via internet'
        self.status = 'desligado'
        self.music = '-----'
        self.music_status = '-------'

        self.commands_description = {
            '1': {'Descrição': 'Ligar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, 
            '2': {'Descrição': 'Desligar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, 
            '3': {'Descrição': 'Setar música', 'Entrada': 'Música', 'Método HTTP': 'PATCH', 'Coleta de dados UDP': False}, 
            '4': {'Descrição': 'Tocar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, 
            '5': {'Descrição': 'Pausar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}}


    def get_query_data(self, server_status: str, id: str) -> str:
        """
        Retorna os dados que devem ser exibidos na opção de "Consultar dados" do dispositivo.

        :param server_status: Indicação do status atual da conexão com o servidor.
        :type server_status: str
        :param id: ID do dispositivo.
        :type id: str
        :return: Dados que devem ser exibidos na opção de "Consultar dados".
        :rtype: dict
        """

        status = self.status.capitalize()
        music = self.music.upper()
        response = {'ID': id,'Status': status, 'Música atual': music, 'Status da música': self.music_status, 'Servidor': server_status}
        return response
    

    def get_status(self) -> str:
        """
        Retorna o status do dispositivo.

        :return: Status do dispositivo.
        :rtype: str
        """

        return self.status
    

    def get_general_description(self) -> dict:
        """
        Retorna os dados quando o Broker pede uma descrição geral do dispositivo.

        :return: Descrição geral do dispositivo.
        :rtype: dict
        """

        status = self.status.capitalize()
        general_description = {'Descrição': self.description, 'Status do dispositivo': status, 'Música atual': self.music, 'Status da música': self.music_status} 
        return general_description


    def get_commands_description(self) -> dict:
        """
        Retorna a descrição de cada comando disponível ao usuário.

        :return: Descrição dos comandos.
        :rtype: dict
        """

        return self.commands_description


    def set_music(self, new_music: str) -> str:
        """
        Seta a nova música. O status da música é modificado para "Tocando" ou "Pausada", dependendo 
        do status atual do dispositivo. Retorna uma mensagem indicando o resultado da operação.

        :param new_music: Nova música a ser setada.
        :type new_music: str
        :return: Resultado da operação.
        :rtype: str
        """

        with threading.Lock():
            self.music = new_music
            if self.status == 'ligado':
                self.music_status = 'Tocando'
            elif self.status == 'desligado':
                self.music_status = 'Pausada'

        return "Música selecionada"
    

    def play_music(self):
        """
        Tenta setar o status da música para "Tocando". Essa ação só é bem sucedida se o dispositivo 
        estiver com o status "Ligado" e a música com o status "Pausada". É retornada a mensagem 
        com o resultado da ação.

        :return: Mensagem que indica o resultado da ação de colocar a música para tocar.
        :rtype: str
        """

        if self.music_status == '-------': 
            return "Nenhuma música foi selecionada"

        else:
            if self.status == 'ligado':

                if self.music_status == 'Tocando':
                    return "A música já está tocando"
                
                elif self.music_status == 'Pausada':
                    with threading.Lock():
                        self.music_status = 'Tocando'
                    return "A música foi colocada para tocar"
                
            elif self.status == 'desligado':
                return "Aparelho desligado, não tem como modificar status da música"
            
            
    def pause_music(self):
        """
        Tenta setar o status da música para "Pausada". Essa ação só é bem sucedida se o dispositivo 
        estiver com o status "Ligado" e a música com o status "Tocando". É retornada a mensagem 
        com o resultado da ação.

        :return: Mensagem que indica o resultado da ação de pausar a música.
        :rtype: str
        """

        if self.music_status == '-------': 
            return "Nenhuma música foi selecionada"

        else:
            if self.status == 'ligado':

                if self.music_status == 'Tocando':
                    with threading.Lock():
                        self.music_status = 'Pausada'
                    return "A música foi pausada"
                
                elif self.music_status == 'Pausada':
                    return "A música já está pausada"
                
            elif self.status == 'desligado':
                return "Aparelho desligado, não tem como modificar status da música"   


    def turn_on(self) -> str:
        """
        Seta o status do dispositivo para "Ligado". Dependendo de qual o status atual, a mensagem de 
        resposta é modificada.

        :return: Mensagem que indica o resultado da ação de ligar o dispositivo.
        :rtype: str
        """

        if self.status == 'desligado':
            with threading.Lock():
                self.status = 'ligado'
                if self.music != '-----':
                    self.music_status = 'Tocando'

            return "Dispositivo ligado"

        else:
            return "Dispositivo já está ligado"
        

    def turn_off(self) -> str:
        """
        Seta o status do dispositivo para "Desligado". Dependendo de qual o status atual, a mensagem de 
        resposta é modificada.

        :return: Mensagem que indica o resultado da ação de desligar o dispositivo.
        :rtype: str
        """

        if self.status == 'ligado':
            with threading.Lock():
                self.status = 'desligado'
                if self.music != '-----':
                    self.music_status = 'Pausada'

            return "Dispositivo desligado"

        else:
            return "Dispositivo já está desligado" 
