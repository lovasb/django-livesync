import os
import itertools
from pathlib import Path

from django.conf import settings
from django.apps import apps
from django.template.utils import get_app_template_dirs

from livesync.core.event import ClientEvent
from livesync.core.signals import livesync_event
from livesync.fswatcher.handlers import BaseEventHandler


class LiveReloadRequestHandler(BaseEventHandler):
    @property
    def watched_paths(self):
        """
        list of paths to be watched for modifications on static files.

        Returns:
        all static and template locations for all apps included in DJANGO_LIVESYNC.INCLUDED_APPS.
        """
        tmpls = []
        for d in get_app_template_dirs(''):
            d = Path(d)
            if Path(settings.BASE_DIR) in d.parents and d.name in settings.DJANGO_LIVESYNC['INCLUDED_APPS'] and (d / 'templates').exists():
                tmpls.append(d / 'templates')

        paths = set(itertools.chain(
            getattr(settings, 'STATICFILES_DIRS', []),
            getattr(settings, 'TEMPLATE_DIRS', []), # django backward compatibility.
            tmpls,
        ))

        paths.update(*[tmpl['DIRS'] for tmpl in settings.TEMPLATES])

        if apps.is_installed('django.contrib.staticfiles'):
            from django.contrib.staticfiles.finders import get_finder
            finder = get_finder('django.contrib.staticfiles.finders.AppDirectoriesFinder')
            paths.update([
                st.location for app, st in finder.storages.items()
                if app in settings.DJANGO_LIVESYNC['INCLUDED_APPS']
            ])

        return paths

    def handle(self, event):
        livesync_event.send(sender=self.__class__, event=ClientEvent(
            action='refresh',
            parameters={}
        ))
