import sys
from tornado.web import Application
from tornado.ioloop import IOLoop

from livesync.core.event import ClientEvent
from livesync.core.signals import livesync_event
from .handler import LiveSyncSocketHandler
from socket import error
import time


class LiveSyncSocketServer(Application):
    def __init__(self,port=9001):
        self.port = port
        super(LiveSyncSocketServer, self).__init__([(r"/", LiveSyncSocketHandler)])

    def server_close(self):
        ioloop = IOLoop.instance()
        ioloop.add_callback(ioloop.stop)
        ioloop.clear_current()
        IOLoop.clear_instance()

    def start(self, started_event=None):
        try:
            self.listen(self.port)
            if started_event:
                # inform the main thread the server can be started.
                started_event.set()
            instance = IOLoop.instance()
            if not instance.asyncio_loop.is_running():
                instance.start()
        except KeyboardInterrupt:
            self.server_close()
            sys.exit(0)
        except error as err:
            if err.errno == 98:
                time.sleep(1)
                livesync_event.send(sender=self.__class__, event=ClientEvent(
                    action='refresh',
                    parameters={}
                ))
                sys.exit(0)
            else:
                sys.exit(1)
