#!/usr/bin/env python
"""
HACK to support the Django + nose without django-nose.
Built based on documentation from:
* https://docs.djangoproject.com/en/1.8/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications
* http://nose.readthedocs.org/en/latest/usage.html#basic-usage
"""
import os
import sys

import nose2
import django
from django.conf import settings
from django.template.utils import get_app_template_dirs

if __name__ == '__main__':
    settings.configure(
        INSTALLED_APPS=['livesync'],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True
        }],
        DJANGO_LIVESYNC={'PORT': 9001, 'HOST': '127.0.0.1', 'EXCLUDED_APPS': {'livesync'}, 'INCLUDED_APPS': []},
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    django.setup()

    result = nose2.discover()
    if not result:
        sys.exit(1)
