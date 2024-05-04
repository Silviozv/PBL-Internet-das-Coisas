import threading  
import __init__

from model.Sensor import Sensor
from model.Connection_device import Connection_device
from impl.sensor.SensorImpl import server_request_tcp, send_data_udp, menu

if __name__=="__main__":

    sensor = Sensor()
    connection = Connection_device()

    # A lógica de receber comandos e poder executar opções do menu parecem funcionar
    threading.Thread(target=server_request_tcp, args=[ sensor, connection]).start()
    threading.Thread(target=send_data_udp, args=[ sensor, connection]).start()
    menu( sensor, connection)
