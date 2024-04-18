from flask import Flask, jsonify, request
import servidor 
import threading

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_id():

    servidor.validate_communication()
    return jsonify(servidor.get_devices_id())

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/description',methods=['GET'])
def get_device_commands_description( device_id):
    servidor.validate_communication()
    return jsonify(servidor.get_device_commands_description(device_id))

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['GET'])
def get_device_data( device_id, command):

    servidor.validate_communication()
    request = {'Comando': command}
    return jsonify(servidor.send_command(device_id, request))

# Enviar comando do tipo mudança de estado
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['POST'])
def set_device_state( device_id, command):

    servidor.validate_communication()
    request = {'Comando': command}
    return jsonify(servidor.send_command(device_id, request))

# Enviar comando do tipo mudar dado específico
@app.route('/devices/<string:device_id>/commands/<string:command>',methods=['PATCH'])
def set_device_data( device_id, command):

    servidor.validate_communication()
    request = {'Comando': command}
    return jsonify(servidor.send_command(device_id, request))

threading.Thread( target=servidor.receive_connection_tcp).start()
threading.Thread( target=servidor.receive_data_udp).start()
app.run(port=5070,host='0.0.0.0')