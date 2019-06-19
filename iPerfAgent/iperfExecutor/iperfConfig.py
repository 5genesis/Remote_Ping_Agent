import re
from typing import List, Dict
from datetime import datetime, timedelta

class iPerfConfig:

    @classmethod
    def formatValidation(cls, parameters: str) -> bool:
        return parameters[0] == '[' and parameters[-1] == ']'

    @classmethod
    def parseParameters(cls, parameters: List[str]) -> Dict:
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
            jsonResult['timestamp'] = int(date.timestamp())
            jsonResult['throughput'] = float(result.group(8))

            if protocol == 'UDP':
                udpResult = re.search(udpPattern, line)
                if udpResult:
                    jsonResult['jitter'] = udpResult.group(1)
                    jsonResult['packetLoss'] = udpResult.group(3)
                else:
                    jsonResult['jitter'] = 0
                    jsonResult['packetLoss'] = 0
            else:
                jsonResult['jitter'] = 0
                jsonResult['packetLoss'] = 0

            if float(result.group(4)) - float(result.group(2)) > 1:
                return None
            else:
                return jsonResult

        return None

