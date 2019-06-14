from flask import Flask, jsonify
from threading import Thread
from iperfExecutor import iPerf
from iperfExecutor.iperfConfig import iPerfConfig

app = Flask(__name__)
iPerf.Initialize(iPerfConfig.IPERF_PATH+'/iperf.exe')


def async_task(clientServer: str, host: str, parameters: str):
    if clientServer == 'Client':
        iPerf.Client(host, parameters)
    else:
        iPerf.Server(parameters)


@app.route('/Client', methods=['GET'])
def BasicClient():
    try:
        Thread(target=async_task, args=('Client', '127.0.0.1', [])).start()
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf client'})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf client', 'Error': f'{error}'}), 403


@app.route('/Server', methods=['GET'])
def BasicServer():
    try:
        Thread(target=async_task, args=('Server', '', [])).start()
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf server'})

    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf server', 'Error': f'{error}'}), 403


@app.route('/Client/<parameters>', methods=['GET'])
def Client(parameters: str):
    if iPerfConfig.formatValidation(parameters):
        try:
            parameters = parameters[1:-1].split(',')
            Thread(target=async_task, args=('Client', '127.0.0.1', parameters)).start()
            return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf client'})

        except RuntimeError as error:
            print(f'{error}')
            return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf client', 'Error': f'{error}'}), 403
    else:
        print(f'Wrong parameters format')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf server',
                        'Error': 'Wrong parameters format.'}), 403


@app.route('/Server/<parameters>', methods=['GET'])
def Server(parameters: str):
    if iPerfConfig.formatValidation(parameters):
        try:
            parameters = parameters[1:-1].split(',')
            Thread(target=async_task, args=('Server', '', parameters)).start()
            return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf server',
                            'Result': iPerf.LastResult()})
        except RuntimeError as error:
            print(f'{error}')
            return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf server', 'Error': f'{error}'}), 403
    else:
        print(f'Wrong parameters format')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf server',
                        'Error': 'Wrong parameters format.'}), 403


@app.route('/Close', methods=['GET'])
def Close():
    try:
        iPerf.Close()
        return jsonify({'Status': 'Success', 'Message': 'Successfully closed iPerf', 'Result': iPerf.LastResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error closing iPerf', 'Error': f'{error}'}), 403


@app.route('/LastResult', methods=['GET'])
def LastResult():
    try:
        iPerf.LastResult()
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last result',
                        'Result': iPerf.LastResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error retrieving last result', 'Error': f'{error}'}), 403


@app.route('/LastError', methods=['GET'])
def LastError():
    try:
        iPerf.LastError()
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last error',
                        'Result': iPerf.LastError()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error retrieving last error', 'Error': f'{error}'}), 403


@app.route('/StartDateTime', methods=['GET'])
def StartDateTime():
    return jsonify({'Status': 'Success', 'Message': f'Start date time {iPerf.StartDateTime()}'})


@app.route('/IsRunning', methods=['GET'])
def IsRunning():
    return jsonify({'Status': 'Success', 'Message': f'iPerf is running: {iPerf.IsRunning()}'})


if __name__ == '__main__':
    app.run()
