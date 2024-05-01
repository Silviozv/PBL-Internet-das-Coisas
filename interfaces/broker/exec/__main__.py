import threading
import __init__
from impl.ServerImpl import receive_connection_tcp, receive_data_udp
from api.API import initialize

if __name__=="__main__":
    
    threading.Thread( target=receive_connection_tcp).start()
    threading.Thread( target=receive_data_udp).start()
    threading.Thread( target=initialize).start()