from iperfExecutor import iPerf


iPerf.Initialize('./iperf3.exe')
iPerf.Client('127.0.0.1', ['-J'])
