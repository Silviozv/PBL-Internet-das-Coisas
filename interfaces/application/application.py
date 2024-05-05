""" 
Módulo contendo as funções de implementação da aplicação. Incluindo: 
a exibição do menu de opções, dependendo do estado atual da aplicação; 
e a lógica de pedidos para a API, dependendo da requisição do usuário.
"""

import requests
import os
import re


def main():
    """
    'Loop' de exibição da tela de menu, mensagens de resposta e 
    pedido de requisição para o usuário. Inicializa as seguintes 
    informações: estado atual do menu do usuário; IP do servidor; 
    informação a ser exibida abaixo das opções de requisição; e a 
    opção atual.
    """
    
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
    """
    Exibe as informações de menu para o usuário. Abaixo das opções 
    de requisição, são exibidas informações de resposta.

    :param info: Armazena todas as informações necessários para a lógica 
    do menu para o usuário.
    :type info: dict
    """

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


def process_option( info: dict) -> dict:
    """
    Processa a opção que o usuário indicou no menu. Dependendo do estado 
    atual do menu, o processamento é feita de forma diferente. 
    A seguir, os estados do menu:

    - Inicial: Menu inicial. Possui apenas as opções de encerrar a 
      aplicação ou setar o IP do servidor desejado;
    - Servidor: Menu de requisições gerais para o Servidor Broker. 
      Podendo requisitar os IPs dos dispositivos conectados ou 
      selecionar um dispositivo para fazer requisições;
    - Dispositivo: Menu de requisições para um dispositivo específico. 
      Pode ser pedida a descrição geral do dispositivo, os comandos 
      disponíveis ao usuário, ou o envio de um comando específico.

    :param info: Armazena todas as informações necessários para a lógica 
    do menu para o usuário.
    :type info: dict
    :return: Informações necessários para a lógica do menu, incluindo a 
    mensagem de resposta em relação a requisição do usuário.
    :rtype: dict
    """

    if ( info['Menu atual'] == 'Inicial'):

        if ( info['Opção'] == '1'):
            server_ip = input("\n  IP do servidor: ").strip()

            try:
                if (not (re.match(r'^(\d{1,3}\.){3}\d{1,3}$', server_ip))):
                    raise ValueError

                url = (f"http://{server_ip}:5070/")
                print("\n  Aguardando resposta do servidor...")
                response_code = requests.head(url, timeout=7).status_code

                if ( response_code == 200):
                    info['Menu atual'] = 'Servidor'
                    info['IP servidor'] = server_ip
                    info['Informação a ser exibida'] = 'Servidor encontrado'
                    return info

            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                info['Informação a ser exibida'] = 'Conexão impossibilitada'
                return info
            except (ValueError) as e:
                info['Informação a ser exibida'] = 'IP inválido'
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
                print("\n  Aguardando resposta do servidor...")
                devices_ip = requests.get(url, timeout=7).json()

                if (len(devices_ip) == 0):
                    info['Informação a ser exibida'] = 'Nenhum dispositivo está conectado'
                    return info

                else:     
                    info['Informação a ser exibida'] = devices_ip
                    return info
            
            elif ( info['Opção'] == '2'):
                device_id = input("\n  ID do dispositivo: ").strip()

                if (not(re.match(r'^DE\d+', device_id))):
                    raise ValueError

                print("\n  Aguardando resposta do servidor...")
                url = (f"http://{info['IP servidor']}:5070/devices")
                devices_id = requests.get(url, timeout=7).json()

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

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            info['Menu atual'] = 'Inicial'
            info['IP servidor'] = ''
            info['Informação a ser exibida'] = 'Conexão encerrada'
            return info
        except (ValueError) as e:
            info['Informação a ser exibida'] = 'ID inválido'
            return info

    elif ( info['Menu atual'] == 'Dispositivo'):
        
        try:
            if ( info['Opção'] == '1'):
                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                print("\n  Aguardando resposta do servidor...")
                response = requests.get(url, timeout=7)
                
                if ( response.status_code == 404):
                    info['Menu atual'] = 'Servidor'
                    info['ID dispositivo'] = ''
                    info['Informação a ser exibida'] = 'Dispositivo desconectado'
                    return info
                
                else:
                    response = response.json()
                    amount_commands = len(response)

                    url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{amount_commands + 1}")
                    response = requests.get(url, timeout=7).json()

                    info['Informação a ser exibida'] =  response['Resposta']
                    return info
            
            elif ( info['Opção'] == '2'):
                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                print("\n  Aguardando resposta do servidor...")
                response = requests.get(url, timeout=7)

                if ( response.status_code == 404):
                    info['Menu atual'] = 'Servidor'
                    info['ID dispositivo'] = ''
                    info['Informação a ser exibida'] = 'Dispositivo desconectado'
                    return info
                
                else:
                    commands_description = {}
                    commands_description_aux = response.json()
                    for key in commands_description_aux:
                        commands_description[key] = commands_description_aux[key]['Descrição']

                    info['Informação a ser exibida'] = commands_description
                    return info
            
            elif ( info['Opção'] == '3'):
                command = input("\n  Comando: ").strip()

                if (not(re.match(r'^\d+$', command))):
                    raise ValueError

                url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/description")
                response = requests.get(url, timeout=7)

                if ( response.status_code == 404):
                    info['Menu atual'] = 'Servidor'
                    info['ID dispositivo'] = ''
                    info['Informação a ser exibida'] = 'Dispositivo desconectado'
                    return info
                
                else:
                    commands_description = response.json()
                    
                    if ( command not in commands_description.keys()):
                        raise ValueError

                    elif ( commands_description[command]['Método HTTP'] == 'GET'):
                        url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}")
                        print("\n  Aguardando resposta do servidor...")
                        response = requests.get(url, timeout=7).json()

                    elif (commands_description[command]['Método HTTP'] == 'POST'):
                        url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}")
                        print("\n  Aguardando resposta do servidor...")
                        response = requests.post(url, timeout=7).json()

                    elif ( commands_description[command]['Método HTTP'] == 'PATCH'):
                        new_data = input(f"  {commands_description[command]['Entrada']}: ").strip()
                        print("\n  Aguardando resposta do servidor...")
                        url = (f"http://{info['IP servidor']}:5070/devices/{info['ID dispositivo']}/commands/{command}/{new_data}")
                        response = requests.patch(url, timeout=7).json()

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

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            info['Menu atual'] = 'Inicial'
            info['IP servidor'] = ''
            info['ID dispositivo'] = ''
            info['Informação a ser exibida'] = 'Conexão encerrada'
            return info
        except (ValueError) as e:
            info['Informação a ser exibida'] = 'Comando inválido'
            return info
        
        
def clear_terminal():
    """
    Limpa os dados da tela de exibição do usuário, adaptando-se ao sistema operacional atual. 
    """

    if os.name == 'nt':  
        os.system('cls')
    else: 
        os.system('clear')
