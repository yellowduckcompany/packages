import asyncio
import logging
import threading

from yellowduck.package import Seatbelt


class Service:

    def __init__(self, package_id):
        self.log = logging.getLogger('seatbelt')
        self.seatbelt = Seatbelt(package_id=package_id)
        self._thread = None

    def start(self):
        """ Start Seatbelt in a separate thread """
        def the_upside_down():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.seatbelt.go())

        self._thread = threading.Thread(target=the_upside_down, daemon=True)
        self._thread.start()

    def stop(self):
        """ Stop Seatbelt """
        self._thread.alive = False
