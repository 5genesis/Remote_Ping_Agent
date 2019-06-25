import json
import pingparsing
from flask import Flask, jsonify
from pingExecutor import ping

app = Flask(__name__)


@app.route('/ping/<address>', methods=['GET'])
def Ping(address: str):
    ping.Ping(address, 0)
    return ""


@app.route('/ping/<address>/size/<packetSize>', methods=['GET'])
def PingCustomSize(address: str, packetSize: int):
    ping.Ping(address, packetSize)
    return ""


if __name__ == '__main__':
    app.run()
