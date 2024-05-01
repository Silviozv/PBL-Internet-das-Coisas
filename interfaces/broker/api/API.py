from flask import Flask, jsonify

import impl.ServerImpl as server

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/',methods=['HEAD'])
def check_connection():

    return '', 200

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_id():
 
    devices_id = server.get_devices_id()
    for i in range(len(devices_id)):
        server.validate_communication(devices_id[i])

    return jsonify(server.get_devices_id()), 200

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/description',methods=['GET'])
def get_device_commands_description( device_id):

    connected = server.validate_communication(device_id)
    if ( connected == True):
        return jsonify(server.get_device_commands_description(device_id)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['GET'])
def get_device_data( device_id, command):

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(server.send_command(device_id, request)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo mudança de estado
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['POST'])
def set_device_state( device_id, command):

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(server.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo mudar dado específico
@app.route('/devices/<string:device_id>/commands/<string:command>/<string:new_data>',methods=['PATCH'])
def set_device_data( device_id, command, new_data):

    connected = server.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command, "Entrada": new_data}
        return jsonify(server.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

def initialize():
    app.run(port=5070,host='0.0.0.0')