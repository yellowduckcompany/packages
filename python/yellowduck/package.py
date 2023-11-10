import sys
import json
import asyncio
import platform

from urllib import request, parse


class Seatbelt:

    def __init__(self, package_id: str):
        self.alive = True
        self._url = 'https://api.yellowduckcompany.com'
        _ver = sys.version_info
        self.whoami = dict(
            package_id=package_id,
            language='python',
            version=f"{_ver.major}.{_ver.minor}.{_ver.micro}",
            platform=platform.system(),
            architecture=platform.machine()
        )

    def service(self, checks):
        data = json.dumps(dict(config=self.whoami, checks=checks))
        h = {'Content-Type': 'application/json'}
        req = request.Request(self._url, data=data, headers=h, method='POST')

        with request.urlopen(req) as rs:
            yield json.loads(rs.read().decode('utf8'))

    async def go(self):
        done = []

        checks = self.service(checks=[])
        for check in checks:
            done.append(check)
        self.service(checks=done)


if __name__ == '__main__':
    task = Seatbelt(package_id=sys.argv[1]).go()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
