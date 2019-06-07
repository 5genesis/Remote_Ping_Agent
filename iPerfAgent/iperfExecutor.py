import subprocess
from typing import List
from datetime import datetime


class iPerf:
    isRunning = False
    executable: str = None
    result: List[str] = []
    startTime: datetime = None

    @classmethod
    def Initialize(cls, executable: str):
        cls.executable = executable

    @classmethod
    def Server(cls, parameters: List[str]):
        params = ['-s', *parameters]
        return cls.execute(params)

    @classmethod
    def Client(cls, host: str, parameters: List[str]):
        params = ['-c', host, *parameters]
        return cls.execute(params)

    @classmethod
    def LastResult(cls):
        return ''.join(cls.result)

    @classmethod
    def StartDateTime(cls):
        return cls.startTime

    @classmethod
    def IsRunning(cls):
        return cls.isRunning

    @classmethod
    def execute(cls, parameters: List[str]) -> int:
        if cls.executable is None:
            raise RuntimeError("Running iPerf without executable")
        if cls.isRunning:
            raise RuntimeError("iPerf already running")

        params = [cls.executable, *parameters]

        cls.isRunning = True
        cls.result = []
        cls.startTime = datetime.now()
        process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cls.stdout(process)
        exitCode = process.wait()
        cls.isRunning = False
        return exitCode

    @classmethod
    def stdout(cls, process: subprocess.Popen):
        pipe = process.stdout

        for line in iter(pipe.readline, b''):
            try: line = line.decode('utf-8').rstrip()
            except Exception as e: line = f"DECODING EXCEPTION: {e}"
            cls.result.append(line)
