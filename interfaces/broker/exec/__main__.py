"""
Módulo de inicialização do Servidor Broker.
"""

import threading
import __init__
from impl.ServerImpl import receive_connection_tcp, receive_data_udp
from api.API import initialize


if __name__=="__main__":
    """
    Inicialização das funções principais do Servidor Broker. Incluindo:
    o recebimento de pedidos de conexão TCP e de dados via comunicação 
    UDP; e a inicialização da API.
    """

    threading.Thread( target=receive_connection_tcp).start()
    threading.Thread( target=receive_data_udp).start()
    threading.Thread( target=initialize).start()