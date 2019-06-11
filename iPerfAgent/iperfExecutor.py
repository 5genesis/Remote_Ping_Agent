import subprocess
import re
from typing import List, Dict
from datetime import datetime
from flask import abort


def parsedParameters(parameters: List[str]) -> Dict:
    params = {}
    for param in parameters:
        param = param.replace('%20', ' ')
        param = param.strip().split(' ')
        k = param[0]
        if len(param) > 1:
            v = param[1]
        else:
            v = ''
        params[k] = v

    return params


class iPerf:
    isRunning = False
    executable: str = None
    result: List[str] = []
    error: List[str] = []
    startTime: datetime = None

    @classmethod
    def Initialize(cls, executable: str):
        cls.executable = executable

    @classmethod
    def Server(cls, parameters: List[str]):
        params = parsedParameters(parameters)
        if '-s' not in params.keys():
            params['-s'] = ""

        return cls.execute(params)

    @classmethod
    def Client(cls, host: str, parameters: List[str]):
        params = parsedParameters(parameters)
        if '-c' not in params.keys():
            params['-c'] = host

        return cls.execute(params)

    @classmethod
    def LastResult(cls):
        try:
            if cls.isRunning:
                raise RuntimeError("iPerf is still running")
            else:
                print(f'Last Result: {cls.result}')

        except RuntimeError as error:
            print(f'Error: {error}')
            abort(403)

        return ''.join(cls.result)

    @classmethod
    def LastError(cls):
        print(f'Last Error: {cls.error}')
        return ''.join(cls.error)


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
        try:
            if cls.executable is None:
                raise RuntimeError('Running iPerf without executable')
            if cls.isRunning:
                raise RuntimeError('iPerf already running')

        except RuntimeError as error:
            print(f'Error: {error}')
            abort(403)

        parametersDict['-f'] = 'M'

        if '-u' in parametersDict.keys() or '-U' in parametersDict.keys():
            protocol = 'UDP'
        else:
            protocol = 'TCP'

        if '-P' in parametersDict.keys():
            parallelEnabled = True
        else:
            parallelEnabled = False

        parameters = []
        for key in parametersDict.keys():
            parameters.append(key)
            parameters.append(parametersDict[key])

        print(parameters)
        params = [cls.executable, *parameters]

        cls.isRunning = True
        cls.result = []
        cls.error = []
        cls.startTime = datetime.now()

        if '-c' in parametersDict.keys():
            print('Client running')
        else:
            print('Server running')
        process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cls.stdout(process, protocol, parallelEnabled)
        exitCode = process.wait()
        cls.isRunning = False
        if '-c' in parametersDict.keys():
            print('Client finished')
            try:
                if cls.error:
                    raise RuntimeError(f'Error: {cls.error}')
            except RuntimeError as error:
                print(f'{error}')
                abort(403)

        return exitCode

    @classmethod
    def stdout(cls, process: subprocess.Popen, protocol: str, parallelEnabled: bool):
        pipe = process.stdout

        for line in iter(pipe.readline, b''):
            try: line = line.decode('utf-8').rstrip()
            except Exception as e: line = f'DECODING EXCEPTION: {e}'
            if 'connect failed' in line or 'error' in line:
                cls.error.append(line)
            if parseIperf(line, protocol, parallelEnabled):
                cls.result.append(line)


def parseIperf(line: str, protocol: str, parallelEnabled: bool):
    pattern = \
        r'\[(.*)] *(\d+(\.\d+)?) *- *(\d+(\.\d+)?) *sec *(\d+(\.\d+)?) *[GKM]Bytes *(\d+(\.\d+)?) *[GKM]Bytes/sec(.*)?'
    # [  3]  0.0-10.0 sec  43591 MBytes  4353 MBytes/sec

    udpPattern = r' *(\d+(\.\d+)?) *ms *\d+ */ *\d+ \((\d+(\.\d+)?)%\) *'
    # [  3]  0.0-10.0 sec  1.25 MBytes  0.13 MBytes/sec   0.026 ms    0/  892 (0%)
    #if protocol == 'UDP':
    #    return re.search(udpPattern, line)
    #else:
    #    return re.search(pattern, line)
    return re.search(pattern, line)
