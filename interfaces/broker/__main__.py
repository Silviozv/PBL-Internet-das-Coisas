import threading
import servidor
import API

if __name__=="__main__":
    
    threading.Thread( target=servidor.receive_connection_tcp).start()
    threading.Thread( target=servidor.receive_data_udp).start()
    threading.Thread( target=API.start).start()