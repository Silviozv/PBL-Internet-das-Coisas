import requests

def initial_menu():
    
    option = input("\n[1] Conectar ao servidor\n[2] Sair\n\n> ")

    while (option != '2'):

        if (option == '1'):
            server_ip = input("\nIP do servidor: ")

            try:
                url = (f'http://{server_ip}:5070/')
                response_code = requests.head(url).status_code

                if ( response_code == 200):
                    server_menu( server_ip)

            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                print("\nConexão Impossibilitada")

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
                print()
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
            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/description')
            response = requests.get(url).json()
            amount_commands = len(response)

            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/{amount_commands + 1}')
            response = requests.get(url).json()

            general_description =  response['Resposta']

            print()
            for key in general_description.keys():
                print(f"{key}: {general_description[key]}")
        
        elif (option == '2'):
            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/description')
            response = requests.get(url).json()
            amount_commands = len(response)

            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/{amount_commands + 2}')
            response = requests.get(url).json()

            available_commands = response['Resposta']

            print()
            for key in available_commands.keys():
                print(f"{key}: {available_commands[key]}")
        
        elif (option == '3'):
            url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/description')
            commands_description = requests.get(url).json()

            command = input("\nComando: ").strip()

            if ( commands_description[command]['Método HTTP'] == 'GET'):
                url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/{command}')
                response = requests.get(url).json()

            elif (commands_description[command]['Método HTTP'] == 'POST'):
                url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/{command}')
                response = requests.post(url).json()

            elif ( commands_description[command]['Método HTTP'] == 'PATCH'):
                url = (f'http://{server_ip}:5070/devices/{device_ip}/commands/{command}')
                response = requests.patch(url).json()

            if ( type(response['Resposta']) == str):
                print(f"\n{response['Resposta']}")

            elif ( type(response['Resposta']) == dict):
                data = response['Resposta']

                print()
                for key in (data.keys()):
                    print(f"{key}: {data[key]}")

        option = input("\n[1] Descrição geral\n[2] Requisições disponíveis\n[3] Enviar requisição\n[4] Voltar\n\n> ")

    return 

def clear_terminal():
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas (Linux, macOS)
        os.system('clear')

if __name__ == "__main__":

    initial_menu()