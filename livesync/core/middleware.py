import re
import json
from django.conf import settings
from django.template.loader import render_to_string


class DjangoLiveSyncMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    @staticmethod
    def process_response(request, response):
        if settings.DEBUG and 'text/html' in response['Content-Type'] and hasattr(response, 'content'):
            livesync_settings = getattr(settings, 'DJANGO_LIVESYNC')
            snippet = render_to_string('livesync/livesync_scripts.html', context={'LIVESYNC_SETTINGS': livesync_settings}).encode('utf-8')

            snippet += b'</body>'
            pattern = re.compile(b'</body>', re.IGNORECASE)
            response.content = pattern.sub(snippet, response.content)

        return response
