import django.dispatch

livesync_event = django.dispatch.Signal(providing_args=["event"])
