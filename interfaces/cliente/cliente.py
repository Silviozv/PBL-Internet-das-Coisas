import requests
import os

def main():
    
    info = {}
    info['Menu atual'] = 'Inicial'
    info['IP servidor'] = ''
    info['ID dispositivo'] = ''
    info['Informação a ser exibida'] = 'Gerenciador iniciado'
    info['Opção'] = ''

    while ( info['Menu atual'] != ''):

        show_screen( info)

        info['Opção'] = input("\n  > ").strip()
        process_option( info)

        clear_terminal()

    return 0 

def show_screen( info: dict):

    print("\n+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")
    print("|                        GERENCIAMENTO DE DISPOSITIVOS                        |")
    print("+-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-+")

    if ( info['Menu atual'] == 'Inicial'):
        menu = {'1': 'CONECTAR AO SERVIDOR', '2': 'SAIR'}
    elif ( info['Menu atual'] == 'Servidor'):
        menu = {'1': 'DISPOSITIVOS CONECTADOS', '2': 'SELECIONAR DISPOSITIVO', '3': 'VOLTAR'}
    elif ( info['Menu atual'] == 'Dispositivo'):
        menu = {'1': 'DESCRIÇÃO GERAL', '2': 'REQUISIÇÕES DISPONÍVEIS', '3': 'ENVIAR REQUISIÇÃO', '4': 'VOLTAR'}

    print("+-----------------------------------------------------------------------------+")
    print("|" + " " * 77 + "|")
    for key in menu.keys():
        text = f"[ {key} ] {menu[key]}"
        space_before = 22
        space_after = 77 - (len(text) + space_before)
        print("|" + " " * space_before + text + " " * space_after + "|")
    print("|" + " " * 77 + "|")
    print("+-----------------------------------------------------------------------------+")

    if ( info['Informação a ser exibida'] != ''):

        print("|" + " " * 77 + "|")

        if ( type(info['Informação a ser exibida']) == str):
            text = info['Informação a ser exibida']
            space_before = (77 - len(text)) // 2
            space_after = 77 - (len(text) + space_before)
            print("|" + " " * space_before + text + " " * space_after + "|")

        elif ( type(info['Informação a ser exibida']) == list):
            for i in range(len(info['Informação a ser exibida'])):
                text = f"{i+1}: {info['Informação a ser exibida'][i]}"
                space_before = 1
                space_after = 77 - (len(text) + space_before)
                print("|" + " " * space_before + text + " " * space_after + "|")

        elif ( type(info['Informação a ser exibida']) == dict):
            for key in info['Informação a ser exibida'].keys():
                text = f"{key}: {info['Informação a ser exibida'][key]}"
                space_before = 1
                space_after = 77 - (len(text) + space_before)
                print("|" + " " * space_before + text + " " * space_after + "|")

        print("|" + " " * 77 + "|")
        print("+-----------------------------------------------------------------------------+")

def process_option( info: dict):

    if ( info['Menu atual'] == 'Inicial'):

        if ( info['Opção'] == '1'):
            server_ip = input("\n  IP do servidor: ").strip()

            try:
                url = (f"http://{server_ip}:5070/")
                response_code = requests.head(url).status_code

                if ( response_code == 200):
                    info['Menu atual'] = 'Servidor'
                    info['IP servidor'] = server_ip
                    info['Informação a ser exibida'] = 'Servidor encontrado'
                    return info

            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                info['Informação a ser exibida'] = 'Conexão impossibilitada'
                return info
            
        elif ( info['Opção'] == '2'):
            info['Menu atual'] = ''
            return info
        
        else:
            info['Informação a ser exibida'] = 'Opção inválida'
            return info

    elif ( info['Menu atual'] == 'Servidor'):
        
        try:
            if ( info['Opção'] == '1'):
                url = (f"http://{info['IP servidor']}:5070/devices")
                devices_ip = requests.get(url).json()

                if (len(devices_ip) == 0):
                    info['Informação a ser exibida'] = 'Nenhum dispositivo está conectado'
                    return info

                else:     
                    info['Informação a ser exibida'] = devices_ip
                    return info
            
            elif ( info['Opção'] == '2'):
                device_id = input("\n  ID do dispositivo: ").strip()

                url = (f"http://{info['IP servidor']}:5070/devices")
                devices_id = requests.get(url).json()

                if (device_id in devices_id):
                    info['Menu atual'] = 'Dispositivo'
                    info['ID dispositivo'] = device_id
                    info['Informação a ser exibida'] = 'Dispositivo selecionado'
                    return info
                
                else:
                    info['Informação a ser exibida'] = 'Dispositivo não encontrado'
                    return info
            
            elif ( info['Opção'] == '3'):
                info['Menu atual'] = 'Inicial'
                info['IP servidor'] = ''
                info['Informação a ser exibida'] = ''
                return info
            
            else:
                info['Informação a ser exibida'] = 'Opção inválida'
                return info
            
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            info['Menu atual'] = 'Inicial'
            info['IP servidor'] = ''
            info['Informação a ser exibida'] = 'Conexão encerrada'
            return info
    
    elif ( info['Menu atual'] == 'Dispositivo'):
        
        try:
            if ( info['Opção'] == '1'):
                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                response = requests.get(url).json()
                amount_commands = len(response)

                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{amount_commands + 1}")
                response = requests.get(url).json()

                info['Informação a ser exibida'] =  response['Resposta']
                return info
            
            elif ( info['Opção'] == '2'):
                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                response = requests.get(url).json()
                amount_commands = len(response)

                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{amount_commands + 2}")
                response = requests.get(url).json()

                info['Informação a ser exibida'] = response['Resposta']
                return info
            
            elif ( info['Opção'] == '3'):
                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                commands_description = requests.get(url).json()

                command = input("\n  Comando: ").strip()

                if ( commands_description[command]['Método HTTP'] == 'GET'):
                    url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}")
                    response = requests.get(url).json()

                elif (commands_description[command]['Método HTTP'] == 'POST'):
                    url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}")
                    response = requests.post(url).json()

                elif ( commands_description[command]['Método HTTP'] == 'PATCH'):
                    new_data = input(f"  {commands_description[command]['Entrada']}: ").strip()
                    url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}/{new_data}")
                    response = requests.patch(url).json()

                info['Informação a ser exibida'] = response['Resposta']
                return info
            
            elif ( info['Opção'] == '4'):
                info['Menu atual'] = 'Servidor'
                info['ID dispositivo'] = ''
                info['Informação a ser exibida'] = ''
                return info
            
            else:
                info['Informação a ser exibida'] = 'Opção inválida'
                return info

        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            info['Menu atual'] = 'Inicial'
            info['IP servidor'] = ''
            info['ID dispositivo'] = ''
            info['Informação a ser exibida'] = 'Conexão encerrada'
            return info

def clear_terminal():
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas (Linux, macOS)
        os.system('clear')

if __name__ == "__main__":

    main()