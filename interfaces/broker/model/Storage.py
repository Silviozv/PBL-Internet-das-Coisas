"""
Módulo contendo a classe que representa o armazenamento do servidor Broker.
"""


class Storage:
    """ Classe que representa o armazenamento do servidor Broker. """

    def __init__(self):
        """
        Inicialização das estruturas de armazenamento do servidor Broker. 
        Descrição das estruturas:

        - connections: Armazena os objetos de comunicação TCP com os dispositivos, 
          usando o IP como chave;
        - connections_id: Armazena o IP dos dispositivos conectados, usando o ID 
          como chave;
        - devices_commands_description: Armazena as informações das requisições de 
          cada dispositivo conectado, usando o IP como chave;
        - data_udp_devices: Armazena os dados recebidos via comunicação UDP, usando 
          o IP como chave;
        - flags_devices: Armazena as 'flags' de controle dos objetos de comunicação TCP, 
          usando o IP como chave.
        """

        self.connections = {}
        self.connections_id = {}
        self.devices_commands_description = {}
        self.data_udp_devices = {}
        self.flags_devices = {}