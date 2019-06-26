import os
import signal
import subprocess
import pingparsing
from textwrap import dedent
from typing import List
from datetime import datetime
from threading import Thread


class ping:
    isRunning = False
    jsonResult: List[str] = []
    error: List[str] = []
    startTime: datetime = None
    processPID: int = -1

    @classmethod
    def Ping(cls, address: str, packetSize: int):
        params = []
        if int(packetSize) > 0:
            params.append('-s')
            params.append(f'{packetSize}')

        params.append(address)

        return cls.execute(params)

    @classmethod
    def Close(cls):
        if not cls.isRunning or cls.processPID == -1:
            raise RuntimeError('ping is not running')

        os.kill(cls.processPID, signal.SIGTERM)
        cls.processPID = -1
        cls.isRunning = False
        return 1

    @classmethod
    def LastJsonResult(cls):
        if cls.isRunning:
            raise RuntimeError("ping is still running")

        print(f'Last Json Result: {cls.jsonResult}')
        return cls.jsonResult

    @classmethod
    def StartDateTime(cls):
        print(f'Start Date Time: {cls.startTime}')
        return cls.startTime

    @classmethod
    def IsRunning(cls):
        print(f'Is Running: {cls.isRunning}')
        return cls.isRunning

    @classmethod
    def execute(cls, parameters: List[str]) -> None:
        if cls.isRunning:
            raise RuntimeError('ping already running')

        params = ['ping', *parameters]
        Thread(target=cls.async_task, args=(params,)).start()
        return None

    @classmethod
    def stdout(cls, process: subprocess.Popen):
        pipe = process.stdout
        pingResult = []
        for line in iter(pipe.readline, b''):
            try:
                line = line.decode('utf-8').rstrip()
            except Exception as e:
                line = f'DECODING EXCEPTION: {e}'

            if 'error' in line or 'failed' in line:
                cls.error.append(line)
            if line != '':
                pingResult.append(line)

        parser = pingparsing.PingParsing()
        pingResult.extend([
            "--- demo.com ping statistics ---",
            "0 packets transmitted, 0 received, 0% packet loss, time 0ms",
            "rtt min/avg/max/mdev = 0.0/0.0/0.0/0.0 ms",
            ])
        stats = parser.parse(dedent("\n".join(pingResult)))

        cls.jsonResult = stats.icmp_replies

    @classmethod
    def async_task(cls, params: List[str]):
        cls.isRunning = True
        cls.error = []
        cls.startTime = datetime.utcnow()
        try:
            process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            cls.processPID = process.pid
            print('ping running')
            cls.stdout(process)
            process.wait()
        except Exception as e:
            print(f'Error in process: {e}')
        finally:
            cls.isRunning = False

        print('ping finished')
