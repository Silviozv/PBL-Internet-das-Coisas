import socket 

# ógica embaralhada
# recebe as conexões; armazena os sockets e printa; o comando de resposta é um rascunho

dispositivos = []

porta_tcp = 5050
ip_local = socket.gethostbyname( socket.gethostname())
print(ip_local)
endereco = (ip_local, porta_tcp)

servidor_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
servidor_tcp.bind( endereco)

servidor_tcp.listen()

def receber_conexao():
    
    while True:

        remetente, endereco_remetente = servidor_tcp.accept()
        dispositivos.append(remetente)
        print("Nova conexao:", endereco_remetente)
        remetente.send("2".encode('utf-8'))
        print(remetente.recv(2048).decode('utf-8'))

receber_conexao()

