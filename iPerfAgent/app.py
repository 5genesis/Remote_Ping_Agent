from flask import Flask
from typing import List
from iPerfAgent.iperfExecutor import iPerf


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/Client', methods=['GET'])
def BasicClient():
    iPerf.Initialize('./iperf.exe')
    iPerf.Client('127.0.0.1', [])
    return ''


@app.route('/Server', methods=['GET'])
def BasicServer():
    iPerf.Initialize('./iperf.exe')
    iPerf.Server([])
    return ''


@app.route('/Client/<parameters>', methods=['GET'])
def Client(parameters: List[str]):
    iPerf.Initialize('./iperf.exe')
    parameters = parameters[1:-1].split(',')
    iPerf.Client('127.0.0.1', parameters)
    return ''


@app.route('/Server/<parameters>', methods=['GET'])
def Server(parameters: List[str]):
    iPerf.Initialize('./iperf.exe')
    parameters = parameters[1:-1].split(',')
    iPerf.Server(parameters)
    return ''


@app.route('/Close', methods=['GET'])
def Close():
    iPerf.Close()
    return ''


@app.route('/LastResult', methods=['GET'])
def LastResult():
    iPerf.LastResult()
    return ''


@app.route('/LastError', methods=['GET'])
def LastError():
    iPerf.LastError()
    return ''


@app.route('/StartDateTime', methods=['GET'])
def StartDateTime():
    iPerf.StartDateTime()
    return ''


@app.route('/IsRunning', methods=['GET'])
def IsRunning():
    iPerf.IsRunning()
    return ''


@app.errorhandler(403)
def forbidden(e):
    return '', 403


if __name__ == '__main__':
    app.run()
