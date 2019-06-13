import os
import signal
import subprocess
from typing import List, Dict
from datetime import datetime
from iperfConfig import iPerfConfig


class iPerf:
    isRunning = False
    executable: str = None
    result: List[str] = []
    error: List[str] = []
    startTime: datetime = None
    isServer = False
    processPID: int = -1

    @classmethod
    def Initialize(cls, executable: str):
        cls.executable = executable

    @classmethod
    def Server(cls, parameters: List[str]):
        params = iPerfConfig.parseParameters(parameters)
        if '-s' not in params.keys():
            params['-s'] = ""

        return cls.execute(params)

    @classmethod
    def Close(cls):
        if not cls.isRunning or cls.processPID == -1:
            raise RuntimeError('iPerf is not running')

        os.kill(cls.processPID, signal.SIGTERM)
        cls.processPID = -1
        cls.isRunning = False
        return 1

    @classmethod
    def Client(cls, host: str, parameters: List[str]):
        params = iPerfConfig.parseParameters(parameters)
        if '-c' not in params.keys():
            params['-c'] = host

        return cls.execute(params)

    @classmethod
    def LastResult(cls):
        if cls.isRunning:
            raise RuntimeError("iPerf is still running")

        print(f'Last Result: {cls.result}')
        return cls.result

    @classmethod
    def LastError(cls):
        if cls.isRunning:
            raise RuntimeError("iPerf is still running")

        print(f'Last Error: {cls.error}')
        return cls.error


    @classmethod
    def StartDateTime(cls):
        print(f'Start Date Time: {cls.startTime}')
        return cls.startTime

    @classmethod
    def IsRunning(cls):
        print(f'Is Running: {cls.isRunning}')
        return cls.isRunning

    @classmethod
    def execute(cls, parametersDict: Dict) -> int:

        if cls.executable is None:
            raise RuntimeError('Running iPerf without executable')
        if cls.isRunning:
            raise RuntimeError('iPerf already running')

        # Force format to MBytes and interval to 1s
        parametersDict['-f'] = 'M'
        parametersDict['-i'] = '1'

        if '-u' in parametersDict.keys() or '-U' in parametersDict.keys():
            protocol = 'UDP'
        else:
            protocol = 'TCP'

        # 'P' parameter must be after client host and port
        if '-P' in parametersDict.keys():
            parallelEnabled = True
            moveToLast = parametersDict.pop('-P')
            parametersDict['-P'] = moveToLast
        else:
            parallelEnabled = False

        parameters = []
        for key in parametersDict.keys():
            parameters.append(key)
            parameters.append(parametersDict[key])

        params = [cls.executable, *parameters]

        cls.isRunning = True
        cls.result = []
        cls.error = []
        cls.startTime = datetime.now()
        process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cls.processPID = process.pid
        if '-c' in parametersDict.keys():
            cls.isServer = False
            print('Client running')
        else:
            cls.isServer = True
            print('Server running')

        cls.stdout(process, protocol, parallelEnabled)
        exitCode = process.wait()
        cls.isRunning = False
        if not cls.isServer:
            print('Client finished')
        else:
            print('Server finished')

        if cls.error:
            raise RuntimeError(f'Error: {cls.error}')

        return exitCode

    @classmethod
    def stdout(cls, process: subprocess.Popen, protocol: str, parallelEnabled: bool):
        pipe = process.stdout

        for line in iter(pipe.readline, b''):

            try: line = line.decode('utf-8').rstrip()
            except Exception as e: line = f'DECODING EXCEPTION: {e}'
            if 'error' in line or 'failed' in line:
                cls.error.append(line)
            if iPerfConfig.parseIperfResult(line, protocol, parallelEnabled):
                cls.result.append(line)
