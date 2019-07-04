from flask import Flask, jsonify
from pingExecutor import ping

app = Flask(__name__)


@app.route('/Ping/<address>', methods=['GET'])
@app.route('/Ping/<address>/Size/<packetSize>', methods=['GET'])
def Ping(address: str, packetSize: int = 0):
    try:
        ping.Ping(address, packetSize)
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed ping'})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing ping', 'Error': f'{error}'}), 403


@app.route('/Close', methods=['GET'])
def Close():
    try:
        ping.Close()
        return jsonify({'Status': 'Success', 'Message': 'Successfully closed ping'})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error closing ping', 'Error': f'{error}'}), 403


@app.route('/LastJsonResult', methods=['GET'])
def LastJsonResult():
    try:
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last json result',
                        'Result': ping.LastJsonResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error retrieving last json result', 'Error': f'{error}'}), 403


@app.route('/StartDateTime', methods=['GET'])
def StartDateTime():
    return jsonify({'Status': 'Success', 'Message': f'Start date time {ping.StartDateTime()}'})


@app.route('/IsRunning', methods=['GET'])
def IsRunning():
    return jsonify({'Status': 'Success', 'Message': f'ping is running: {ping.IsRunning()}'})


if __name__ == '__main__':
    app.run()
