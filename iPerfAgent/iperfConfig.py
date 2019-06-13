import re
from typing import List, Dict


class iPerfConfig:
    IPERF_PATH = 'C:/Users/Gonzalo/Documents/iperf.exe'

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
    def parseIperfResult(cls, line: str, protocol: str, parallelEnabled: bool):
        pattern = r'\[(.*)] *(\d+(\.\d+)?) *- *(\d+(\.\d+)?) *sec *(\d+(\.\d+)?) *[GKM]Bytes *(\d+(\.\d+)?) *[GKM]Bytes/sec(.*)?'
        # [  3]  0.0-10.0 sec  44712 MBytes  4468 MBytes/sec

        udpPattern = r' *(\d+(\.\d+)?) *ms *\d+ */ *\d+ \((\d+(\.\d+)?)%\) *'
        # [  3]  0.0-10.0 sec  1.25 MBytes  0.12 MBytes/sec   0.024 ms    0/  893 (0%)

        result = re.search(pattern, line)
        if result and protocol == 'UDP':
            result = re.search(udpPattern, line)

        if result and parallelEnabled:
            result = 'SUM' in line
        # [SUM]  0.0-10.0 sec  102153 MBytes  10202 MBytes/sec

        return result

