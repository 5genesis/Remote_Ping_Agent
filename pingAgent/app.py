from flask import Flask, jsonify, request
from pingExecutor import ping

app = Flask(__name__)


@app.route('/Ping/<address>', methods=['GET'])
def Ping(address: str):
    try:
        interval = float(request.args.get('interval', 1.0))
        size = int(request.args.get('size', 0))
        ttl = int(request.args.get('ttl', 0))
        ping.Ping(address, interval, size, ttl)
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed ping'})
    except Exception as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing ping', 'Error': f'{error}'}), 403


@app.route('/Close', methods=['GET'])
def Close():
    try:
        ping.Close()
        return jsonify({'Status': 'Success', 'Message': 'Successfully closed ping'})
    except Exception as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error closing ping', 'Error': f'{error}'}), 403


@app.route('/LastJsonResult', methods=['GET'])
def LastJsonResult():
    try:
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last json result',
                        'Result': ping.LastJsonResult()})
    except Exception as error:
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
