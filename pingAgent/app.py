from flask import Flask, jsonify
from pingExecutor import ping

app = Flask(__name__)


@app.route('/ping/<address>', methods=['GET'])
@app.route('/ping/<address>/size/<packetSize>', methods=['GET'])
def Ping(address: str, packetSize: int = 0):
    ping.Ping(address, packetSize)
    return ""


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
        ping.LastJsonResult()
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
