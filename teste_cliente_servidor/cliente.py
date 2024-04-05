import socket

PORTA = 5050
servidor = "172.17.0.2"
ADDR = (servidor, PORTA)

cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(ADDR)

def send(msg):

    msg = msg.encode("utf-8")
    cliente.send(msg)
    print(cliente.recv(8).decode("utf-8"))


send("olaaa")