from flask import Flask, jsonify, request
import servidor 
import threading

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_ip():

    return jsonify(servidor.get_devices_ip())

# Consultar comandos disponíveis de um dispositivo
@app.route('/devices/<string:device_ip>/commands',methods=['GET'])
def get_device_commands( device_ip):

    return jsonify(servidor.get_available_commands(device_ip))

# Consultar descrição geral do dispositivo
@app.route('/devices/<string:device_ip>/description',methods=['GET'])
def get_device_description( device_ip):

    return jsonify(servidor.get_general_description(device_ip))

# Modificar status do dispositivo
@app.route('/devices/<string:device_ip>/status/<string:command>',methods=['PATCH'])
def set_device_status( device_ip, command):

    if ( command == 'ligar'):

        response = servidor.turn_on_device(device_ip)

        if ( response == 'Dispositivo ligado'):
            return jsonify(servidor.get_general_description(device_ip)), 200
        
        elif ( response == 'Dispositivo já está ligado'): 
            return jsonify(servidor.get_general_description(device_ip)), 422
    
    elif ( command == 'desligar'):

        response = servidor.turn_off_device(device_ip)

        if ( response == 'Dispositivo desligado'):
            return jsonify(servidor.get_general_description(device_ip)), 200
        
        elif ( response == 'Dispositivo já está desligado'): 
            return jsonify(servidor.get_general_description(device_ip)), 422

# Consultar tipo do dispositivo
@app.route('/devices/<string:device_ip>/type',methods=['GET'])
def get_device_type( device_ip):

    return jsonify(servidor.get_device_type( device_ip)), 200
    
# Consultar tipo do dispositivo
@app.route('/devices/<string:device_ip>/data',methods=['GET'])
def get_device_data( device_ip):

    response = servidor.get_data_udp(device_ip)

    if ( response == "Dispositivo desligado, não é possível coletar dados de leitura"):

        return jsonify({"Resposta": "Dispositivo desligado, não é possível coletar dados de leitura"}), 404

    else:

        return jsonify(response), 200

# Consultar tipo do dispositivo
@app.route('/devices/<string:device_ip>/data/<string:data>',methods=['PATCH'])
def set_device_data( device_ip, data):

    response = servidor.set_data( device_ip, data)

    if ( response == "Dado selecionado"):

        return jsonify(servidor.get_general_description(device_ip)), 200



threading.Thread( target=servidor.receive_connection_tcp).start()
threading.Thread( target=servidor.receive_data_udp).start()
app.run(port=5070,host='0.0.0.0')