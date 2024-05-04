"""
Módulo de inicialização do Sensor de temperatura.
"""

import threading  
import __init__

from model.Sensor import Sensor
from model.Connection_device import Connection_device
from impl.sensor.SensorImpl import server_request_tcp, send_data_udp, menu


if __name__=="__main__":
    """
    Inicialização das funções principais do dispositivo, e declaração dos objetos de 
    representação do Sensor de temperatura e da sua conexão com o servidor.
    """

    sensor = Sensor()
    connection = Connection_device()

    threading.Thread(target=server_request_tcp, args=[ sensor, connection]).start()
    threading.Thread(target=send_data_udp, args=[ sensor, connection]).start()
    menu( sensor, connection)
