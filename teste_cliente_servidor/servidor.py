import socket

PORTA = 5050
IP_LOCAL = socket.gethostbyname( socket.gethostname())
ADDR = (IP_LOCAL, PORTA)

print(f"IP: {IP_LOCAL}")

servidor = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
servidor.bind( ADDR)

def logica_cliente ( conn, addr):
    
    print(f"Nova conexão: {addr}")

    while True:
        msg = conn.recv(5).decode("utf-8")

        if msg:
            print("mensagem:", msg)
            conn.send("Recebido".encode("utf-8"))


def start ():

    servidor.listen()

    while True:

        conn, addr = servidor.accept()

        logica_cliente(conn, addr)

print("Servidor iniciando...")
start()