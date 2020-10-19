import os
import re
import signal
import subprocess
import pingparsing
from textwrap import dedent
from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone
from threading import Thread
from pprint import pprint


class ping:
    isRunning = False
    jsonResult: Dict = {}
    error: List[str] = []
    startTime: datetime = None
    processPID: Optional[int] = None

    @classmethod
    def Ping(cls, address: str, interval: float, size: int, ttl: int):
        params = ['-i', str(interval), '-O']
        if size > 0:
            params.extend(['-s', str(size)])
        if ttl > 0:
            params.extend(['-t', str(ttl)])
        params.append(address)

        return cls.execute(params, interval)

    @classmethod
    def Close(cls):
        if not cls.isRunning or cls.processPID is None:
            raise RuntimeError('ping is not running')
        os.kill(cls.processPID, signal.SIGTERM)

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
    def execute(cls, parameters: List[str], interval: float) -> None:
        if cls.isRunning:
            raise RuntimeError('ping already running')

        params = ['ping', *parameters]
        print(f'Final CLI paramenters: {params}')
        Thread(target=cls.async_task, args=(params, interval)).start()
        return None

    @classmethod
    def stdout(cls, process: subprocess.Popen, interval: float):
        pipe = process.stdout
        pingResult = []
        lostPings = []

        for line in iter(pipe.readline, b''):
            try:
                line = line.decode('utf-8').rstrip()
            except Exception as e:
                line = f'DECODING EXCEPTION: {e}'

            print(line)

            if 'error' in line or 'failed' in line:
                cls.error.append(line)

            result = re.search(r'no answer yet for icmp_seq=(\d+)', line)
            if result:
                lost_seq = int(result.group(1))
                lostPings.append(lost_seq)

            if line != '':
                pingResult.append(line)

        parser = pingparsing.PingParsing()
        pingResult.extend([
            "--- demo.com ping statistics ---",
            "0 packets transmitted, 0 received, 0% packet loss, time 0ms",
            "rtt min/avg/max/mdev = 0.0/0.0/0.0/0.0 ms",
        ])
        stats = parser.parse(dedent("\n".join(pingResult)))
        icmp_replies = stats.icmp_replies

        for lost in lostPings:
            icmp_replies.insert(lost-1, {'timestamp': None, 'icmp_seq': lost, 'ttl': 54, 'time': -1.0,
                                         'duplicate': False})
        for icmp in icmp_replies:
            date = cls.startTime + timedelta(seconds=(icmp['icmp_seq']*interval))
            icmp['timestamp'] = date.timestamp()

        cls.jsonResult = {'total': len(icmp_replies), 'success': len(icmp_replies)-len(lostPings),
                          'icmp_replies': icmp_replies}

        print("Final JSON results")
        pprint(cls.jsonResult)

    @classmethod
    def async_task(cls, params: List[str], interval: float):
        cls.isRunning = True
        cls.error = []
        cls.startTime = datetime.now(timezone.utc)
        try:
            process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            cls.processPID = process.pid
            print('ping running')
            cls.stdout(process, interval)
            process.wait()
        except Exception as e:
            print(f'Error in process: {e}')
        finally:
            cls.isRunning = False
            cls.processPID = None

        print('ping finished')
