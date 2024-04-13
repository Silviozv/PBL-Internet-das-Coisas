import requests
import json

def initial_menu():
    
    option = input("\n[1] Conectar ao servidor\n[2] Sair\n\n> ")

    while (option != '2'):

        if (option == '1'):
            server_ip = input("\nIP do servidor: ")
            server_menu( server_ip)

        option = input("\n[1] Conectar ao servidor\n[2] Sair\n\n> ")

    return 

def server_menu( server_ip: str):

    option = input("\n[1] Dispositivos conectados\n[2] Selecionar dispositivo\n[3] Voltar\n\n> ")

    while (option != '3'):

        if (option == '1'):

            url = (f'http://{server_ip}:5070/devices')
            devices_ip = requests.get(url).json()

            if (len(devices_ip) == 0):
                print("\nNenhum dispositivo está conectado")

            else:
                
                print("\n")
                for i in range(len(devices_ip)):
                    print(f"{i+1}: {devices_ip[i]}")

        elif (option == '2'):

            device_ip = input("\nIP do dispositivo: ")
            device_menu( server_ip, device_ip)
        
        option = input("\n[1] Dispositivos conectados\n[2] Selecionar dispositivo\n[3] Voltar\n\n> ")

    return 

    
def device_menu(server_ip: str, device_ip: str):

    option = input("\n[1] Descrição geral\n[2] Requisições disponíveis\n[3] Enviar requisição\n[4] Voltar\n\n> ")

    while (option != '4'):

        if (option == '1'):
            pass
        
        elif (option == '2'):
            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands')
            available_commands = requests.get(url).json()

            print("\n")
            for i in range(len(available_commands)):
                print(f"{i+1}: {available_commands[i]}")
        
        elif (option == '3'):
            pass

        option = input("\n[1] Descrição geral\n[2] Requisições disponíveis\n[3] Enviar requisição\n[4] Voltar\n\n> ")

    return 


if __name__ == "__main__":

    initial_menu()