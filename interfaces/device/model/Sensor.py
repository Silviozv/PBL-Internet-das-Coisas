"""
Módulo contendo a classe do sensor de tempetarura.
"""

import socket
import threading


class Sensor:
    """ Classe que representa um sensor de temperatura. """


    def __init__(self):
        """
        Inicialização dos atributos base do sensor de temperatura. Incluindo: a descrição, o status, os 
        dados da temperatura, e as descrições dos comandos disponíveis para requisição..
        """

        self.description = 'Sensor de temperatura'
        self.status = 'desligado'
        self.temperature = '-----'

        self.commands_description = {
            '1': {'Descrição': 'Ligar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, 
            '2': {'Descrição': 'Desligar', 'Entrada': '', 'Método HTTP': 'POST', 'Coleta de dados UDP': False}, 
            '3': {'Descrição': 'Retornar medida de temperatura', 'Entrada': '', 'Método HTTP': 'GET', 'Coleta de dados UDP': True}}


    def get_query_data(self, server_status: str, id: str) -> dict:
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
        response = {'ID': id,'Status': status, 'Temperatura': self.temperature, 'Servidor': server_status}
        return response


    # Dados a serem enviados via UDP
    def get_returning_data(self) -> dict:
        """
        Retorna o dado que deve ser enviado periodicamente via comunicação UDP.

        :return: Dados enviados via comunicação UDP.
        :rtype: dict
        """

        data = {"Temperatura": self.temperature}
        return data
    

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
        general_description = {'Descrição': self.description, 'Status': status} 
        return general_description
    

    def get_commands_description(self) -> dict:
        """
        Retorna a descrição de cada comando disponível para requisição.

        :return: Descrição dos comandos.
        :rtype: dict
        """

        return self.commands_description


    def set_temperature(self) -> str:
        """
        Pede uma nova medida de temperatura e checa se é um valor válido. Se for, seta como a nova 
        medida de temperatura do sensor. É retornado se a operação foi bem sucedida ou não.

        :return: Mensagem que indica o resultado da ação de mudança de temperatura.
        :rtype: str
        """

        try:
            new_temperature = int(input("\n  Temperatura: "))

            if -50 < new_temperature < 300:
                self.temperature = (f'{new_temperature}°C')
                return "Medida de temperatura atualizada"
            else:
                raise ValueError
            
        except (ValueError) as e:
            return "Valor inválido"


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

            return "Dispositivo desligado"

        else:
            return "Dispositivo já está desligado" 
