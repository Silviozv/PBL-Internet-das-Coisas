from flask import Flask, jsonify, request
import servidor 
import threading

app = Flask(__name__)

# Consultar todos os IPs
@app.route('/devices/',methods=['GET'])
def get_devices_ip():

    return jsonify(servidor.get_devices_ip())

# Consultar todos os IPs
@app.route('/devices/<string:device_ip>/commands',methods=['GET'])
def get_device_commands( device_ip):

    return jsonify(servidor.get_available_commands(device_ip))


threading.Thread( target=servidor.receive_connection_tcp).start()
threading.Thread( target=servidor.receive_data_udp).start()
app.run(port=5070,host='0.0.0.0')