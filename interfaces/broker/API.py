from flask import Flask, jsonify
import servidor 
import threading

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/',methods=['HEAD'])
def check_connection():

    return '', 200

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_id():

    devices_id = servidor.get_devices_id()
    for i in range(len(devices_id)):
        servidor.validate_communication(devices_id[i])

    return jsonify(servidor.get_devices_id()), 200

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/description',methods=['GET'])
def get_device_commands_description( device_id):

    connected = servidor.validate_communication(device_id)
    if ( connected == True):
        return jsonify(servidor.get_device_commands_description(device_id)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['GET'])
def get_device_data( device_id, command):

    connected = servidor.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(servidor.send_command(device_id, request)), 200
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo mudança de estado
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['POST'])
def set_device_state( device_id, command):

    connected = servidor.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command}
        return jsonify(servidor.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

# Enviar comando do tipo mudar dado específico
@app.route('/devices/<string:device_id>/commands/<string:command>/<string:new_data>',methods=['PATCH'])
def set_device_data( device_id, command, new_data):

    connected = servidor.validate_communication(device_id)
    if ( connected == True):
        request = {'Comando': command, "Entrada": new_data}
        return jsonify(servidor.send_command(device_id, request))
    elif ( connected == False):
        return jsonify ({'Resposta': 'Dispositivo não encontrado'}), 404

def start():
    app.run(port=5080,host='0.0.0.0')