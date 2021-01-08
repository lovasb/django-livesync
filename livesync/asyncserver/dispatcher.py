import json
from threading import Timer

from django.dispatch import receiver
from websocket import create_connection
from django.conf import settings

from livesync.core.signals import livesync_event

EVENTS = {
    'refresh': {"action": "refresh"}
}


@receiver(livesync_event)
def dispatch(event, **kwargs):
    uri = "ws://{host}:{port}".format(
        host=settings.DJANGO_LIVESYNC['HOST'],
        port=settings.DJANGO_LIVESYNC['PORT'])

    connection = create_connection(uri)
    if hasattr(event, '__iter__'):
        event = json.dumps(dict(event))
    elif isinstance(event, str):
        event = json.dumps(EVENTS[event])
    else:
        raise NotImplementedError

    connection.send(event)
    connection.close()
