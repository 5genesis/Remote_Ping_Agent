import os
import yaml
from flask import Flask, jsonify
from typing import List
from iperfExecutor import iPerf
from iperfExecutor.iperfConfig import iPerfConfig

app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(THIS_FOLDER, 'config.yml'), 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

iPerf.Initialize(data['IPERF_PATH'])


def runIperf(clientServer: str, host: str, parameters: List[str]):
    if clientServer == 'Client':
        iPerf.Client(host, parameters)
    else:
        iPerf.Server(parameters)


@app.route('/Client', methods=['GET'])
def BasicClient():
    try:
        runIperf('Client', '127.0.0.1', [])
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf client'})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf client', 'Error': f'{error}'}), 403


@app.route('/Server', methods=['GET'])
def BasicServer():
    try:
        runIperf('Server', '', [])
        return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf server'})

    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error executing iPerf server', 'Error': f'{error}'}), 403


@app.route('/Client/<parameters>', methods=['GET'])
def Client(parameters: str):
    if iPerfConfig.formatValidation(parameters):
        try:
            parameters = parameters[1:-1].split(',')
            runIperf('Client', '127.0.0.1', parameters)
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
            runIperf('Server', '', parameters)
            return jsonify({'Status': 'Success', 'Message': 'Successfully executed iPerf server',
                            'Result': iPerf.LastRawResult()})
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
        return jsonify({'Status': 'Success', 'Message': 'Successfully closed iPerf', 'Result': iPerf.LastRawResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error closing iPerf', 'Error': f'{error}'}), 403


@app.route('/LastRawResult', methods=['GET'])
def LastRawResult():
    try:
        iPerf.LastRawResult()
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last raw result',
                        'Result': iPerf.LastRawResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error retrieving last raw result', 'Error': f'{error}'}), 403


@app.route('/LastJsonResult', methods=['GET'])
def LastJsonResult():
    try:
        iPerf.LastJsonResult()
        return jsonify({'Status': 'Success', 'Message': 'Successfully retrieved last json result',
                        'Result': iPerf.LastJsonResult()})
    except RuntimeError as error:
        print(f'{error}')
        return jsonify({'Status': 'Error', 'Message': 'Error retrieving last json result', 'Error': f'{error}'}), 403


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
