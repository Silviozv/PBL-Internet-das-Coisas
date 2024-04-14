from flask import Flask, jsonify, request
import servidor 
import threading

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_ip():

    return jsonify(servidor.get_devices_ip())

# Enviar comando do tipo de retorno de dados
@app.route('/devices/<string:device_ip>/commands/<string:command>',methods=['GET'])
def get_device_data( device_ip, command):

    request = {'Comando': command}
    return jsonify(servidor.send_command(device_ip, request))

# Enviar comando do tipo mudança de estado
@app.route('/devices/<string:device_ip>/commands/<string:command>',methods=['POST'])
def set_device_state( device_ip, command):

    request = {'Comando': command}
    return jsonify(servidor.send_command(device_ip, request))

# Enviar comando do tipo mudar dado específico
@app.route('/devices/<string:device_ip>/commands/<string:command>',methods=['PATCH'])
def set_device_data( device_ip, command):

    request = {'Comando': command}
    return jsonify(servidor.send_command(device_ip, request))

threading.Thread( target=servidor.receive_connection_tcp).start()
threading.Thread( target=servidor.receive_data_udp).start()
app.run(port=5070,host='0.0.0.0')