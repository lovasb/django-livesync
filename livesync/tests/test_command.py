import unittest
from django.conf import settings
from django.core.management.base import CommandError
from django.test import override_settings

from livesync.management.commands.runserver import Command
from livesync.core.handler import LiveReloadRequestHandler


class MockEventHandler:
    @property
    def watched_paths(self):
        return []


class OptionsParserTestcase(unittest.TestCase):
    def setUp(self):
        self.command = Command()

    def tearDown(self):
        settings.DJANGO_LIVESYNC = dict()

    def test_parse_default_options(self):
        options = {'liveport': None, 'addrport': ''}
        self.command._parse_options(**options)

        self.assertEqual(self.command.liveport, 9001)
        self.assertEqual(self.command.livehost, 'localhost')

    def test_parse_custom_port_and_host(self):
        options = {'liveport': 8888, 'addrport': '0.0.0.0:8000'}
        self.command._parse_options(**options)

        self.assertEqual(self.command.liveport, 8888)
        self.assertEqual(self.command.livehost, '0.0.0.0')

    def test_parse_invalid_port_raises_command_error(self):
        options = {'liveport': 'abc', 'addrport': ''}

        with self.assertRaises(CommandError):
            self.command._parse_options(**options)

    def test_default_event_handler(self):
        self.command._start_watchdog()
        handler, = self.command.file_watcher.handlers
        self.assertIsInstance(handler, LiveReloadRequestHandler)

    @override_settings(DJANGO_LIVESYNC={'EVENT_HANDLER': 'livesync.tests.test_command.MockEventHandler'})
    def test_customize_event_handler(self):
        self.command._start_watchdog()
        handler, = self.command.file_watcher.handlers
        self.assertIsInstance(handler, MockEventHandler)
