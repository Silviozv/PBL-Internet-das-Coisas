"""
Módulo de inicialização do Radio.
"""

import threading  
import __init__

from model.Radio import Radio
from model.Connection_device import Connection_device
from impl.RadioImpl import server_request_tcp, menu


if __name__=="__main__":
    """
    Inicialização das funções principais do dispositivo, e declaração dos objetos de 
    representação do Radio e da sua conexão com o servidor.
    """

    radio = Radio()
    connection = Connection_device()

    threading.Thread(target=server_request_tcp, args=[ radio, connection]).start()
    menu( radio, connection)
