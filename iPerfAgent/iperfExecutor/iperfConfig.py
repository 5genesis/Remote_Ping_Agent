import re
from typing import List, Dict
from datetime import datetime, timedelta


class iPerfConfig:
    longParameters = {
        "--bandwidth": "-b",
        "--bind": "-B",
        "--client": "-c",  # for iPerf Server
        "--compatibility": "-C",
        "--dualtest": "-d",
        "--format": "-f",
        "--interval": "-i",
        "--len": "-l",
        "--listenport": "-L",
        "--print_mss": "-m",
        "--mss": "-M",
        "--num": "-n",
        "--nodelay": "-N",
        "--port": "-p",
        "--tradeoff": "-r",
        "--tos": "-S",
        "--time": "-t",
        "--ttl": "-T",
        "--udp": "-u",
        "--window": "-w"
    }

    @classmethod
    def formatValidation(cls, parameters: str) -> bool:
        return parameters[0] == '[' and parameters[-1] == ']'

    @classmethod
    def parseParameters(cls, parameters: List[str]) -> Dict:
        params = {}
        for param in parameters:
            if ':' not in param:
                param = param.strip().replace(' ', ': ')
            param = param.strip().split(': ')
            k = param[0]
            if len(param) > 1:
                v = param[1]
            else:
                v = ''
            params[k] = v

        return params

    @classmethod
    def shortenParameters(cls, parameters: Dict) -> Dict:
        print(parameters)
        shortParameters = parameters
        for param in parameters.keys():
            if param in cls.longParameters.keys():
                value = shortParameters[param]
                shortParameters.pop(param)
                shortParameters[cls.longParameters[param]] = value

        print(shortParameters)
        return shortParameters

    @classmethod
    def parseIperfResult(cls, line: str, protocol: str, parallelEnabled: bool, startTime: datetime):
        pattern = r'\[(.*)] *(\d+(\.\d+)?) *- *(\d+(\.\d+)?) *sec *(\d+(\.\d+)?) *[GKM]Bytes *(\d+(\.\d+)?) *[GKM]Bytes/sec(.*)?'
        # [  3]  0.0-10.0 sec  44712 MBytes  4468 MBytes/sec
        udpPattern = r' *(\d+(\.\d+)?) *ms *\d+ */ *\d+ \((\d+(\.\d+)?)%\) *'
        # [  3]  0.0-10.0 sec  1.25 MBytes  0.12 MBytes/sec   0.024 ms    0/  893 (0%)
        jsonResult = {}
        result = re.search(pattern, line)
        if result:
            instanceId = str(result.group(1))

            if parallelEnabled and instanceId != 'SUM':
                return None

            second = int(float(result.group(2)))
            date = startTime + timedelta(seconds=second)
            jsonResult['timestamp'] = date.timestamp()
            jsonResult['throughput'] = float(result.group(8))

            udpResult = re.search(udpPattern, line)

            if protocol == 'UDP' and udpResult:
                    jsonResult['jitter'] = udpResult.group(1)
                    jsonResult['packetLoss'] = udpResult.group(3)
            else:
                jsonResult['jitter'] = 0
                jsonResult['packetLoss'] = 0

            if float(result.group(4)) - float(result.group(2)) > 1:
                return None
            else:
                return jsonResult

        return None

