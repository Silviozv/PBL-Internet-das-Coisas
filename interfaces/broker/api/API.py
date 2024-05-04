""" 
Módulo contendo os endereços da API e a sua função de inicialização.
"""

from flask import Flask, jsonify
import impl.ServerImpl as server

"""
Declarando objeto contendo a implementação da API.
"""
app = Flask(__name__)


@app.route('/',methods=['HEAD'])
def check_connection():
    """
    Verifica se a API está online.
    """

    return '', 200


@app.route('/devices/',methods=['GET'])
def get_devices_id():
    """
    Retorna a lista de IDs conectados ao Servidor Broker. É feita 
    a verificação de conexão com cada dispositivo antes de retornar 
    os IDs. Se nenhum estiver conectado, é retornada a lista vazia.

    Returns:
        list: Lista contendo os IDs dos dispositivos conectados.
            Exemplo: ["DE11", "DE12", "DE13"]
    """
 
    devices_id = server.get_devices_id()
    for i in range(len(devices_id)):
        server.validate_communication(devices_id[i])

    return jsonify(server.get_devices_id()), 200


@app.route('/devices/<string:device_id>/commands/description',methods=['GET'])
def get_device_commands_description( device_id):
    """
    Retorna as descrições dos comandos do dispositivo. É feita 
    a verificação de conexão com o dispositivo antes de retornar 
    os dados.

    Args:
        device_id (str): ID do dispositivo.

    Returns:
        dict: Dicionário contendo as descrições dos comandos.
            Exemplo:
            {
                "Resposta": 
                {
                    "1": 
                    {
                        "Entrada": "Música"
                        "Método HTTP": "PATCH"
                        "Coleta de dados UDP": False
                    }
                    "2": 
                    {
                        "Entrada": ""
                        "Método HTTP": "GET"
                        "Coleta de dados UDP": True
                    }  
                }
            }

    Raises:
        NotFound: Dispositivo não encontrado.
    """

    connected = server.validate_communication(device_id)
    if ( connected == True):
        return jsonify(server.get_device_commands_description(device_id)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404


@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['GET'])
def get_device_data( device_id, command):
    """
    Envia o comando de requisição de coleta de dado para o 
    Servidor Broker e retorna a resposta recebida. É feita a 
    verificação de conexão com o dispositivo antes de enviar 
    a requisição.

    Args:
        device_id (str): ID do dispositivo.
        command (str): Comando.

    Returns:
        dict: Dicionário contendo a resposta do dispositivo.
            Exemplo:
            {
                "Resposta": 
                {
                    "Temperatura": "89 °C"
                }
            }

    Raises:
        NotFound: Dispositivo não encontrado.
    """

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(server.send_command(device_id, request)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404


@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['POST'])
def set_device_state( device_id, command):
    """
    Envia o comando de requisição para alterar o estado de algum 
    dado do dispositivo, sem necessidade de uma entrada explícita. 
    É feita a verificação de conexão com o dispositivo antes de  
    enviar a requisição.

    Args:
        device_id (str): ID do dispositivo.
        command (str): Comando.

    Returns:
        dict: Dicionário contendo a resposta do dispositivo.
            Exemplo:
            {
                "Resposta": "Dispositivo ligado"
            }

    Raises:
        NotFound: Dispositivo não encontrado.
    """

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(server.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404


# Enviar comando do tipo mudar dado específico
@app.route('/devices/<string:device_id>/commands/<string:command>/<string:new_data>',methods=['PATCH'])
def set_device_data( device_id, command, new_data):
    """
    Envia o comando de requisição para alterar o dado de alguma 
    informação do dispositivo, precisando da indicação do novo dado. 
    É feita a verificação de conexão com o dispositivo antes de  
    enviar a requisição.

    Args:
        device_id (str): ID do dispositivo.
        command (str): Comando.
        new_data (str): Novo dado que deve ser setado.

    Returns:
        dict: Dicionário contendo a resposta do dispositivo.
            Exemplo:
            {
                "Resposta": "Música selecionada"
            }

    Raises:
        NotFound: Dispositivo não encontrado.
    """

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command, "Entrada": new_data}
        return jsonify(server.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404


def initialize():
    """
    Inicialização da API.
    """

    app.run(port=5070,host='0.0.0.0')
