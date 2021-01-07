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
    @override_settings(DJANGO_LIVESYNC={})
    def test_parse_default_options(self):
        command = Command()
        options = {'liveport': None, 'addrport': ''}
        command._parse_options(**options)

        self.assertEqual(command.liveport, 9001)
        self.assertEqual(command.livehost, 'localhost')

    def test_parse_custom_port_and_host(self):
        command = Command()
        options = {'liveport': 8888, 'addrport': '0.0.0.0:8000'}
        command._parse_options(**options)

        self.assertEqual(command.liveport, 8888)
        self.assertEqual(command.livehost, '0.0.0.0')

    def test_parse_invalid_port_raises_command_error(self):
        command = Command()
        options = {'liveport': 'abc', 'addrport': ''}

        with self.assertRaises(CommandError):
            command._parse_options(**options)

    def test_default_event_handler(self):
        command = Command()
        command._start_watchdog()
        handler, = command.file_watcher.handlers
        self.assertIsInstance(handler, LiveReloadRequestHandler)

    @override_settings(DJANGO_LIVESYNC={'EVENT_HANDLER': 'livesync.tests.test_command.MockEventHandler'})
    def test_customize_event_handler(self):
        command = Command()
        command._start_watchdog()
        handler, = command.file_watcher.handlers
        self.assertIsInstance(handler, MockEventHandler)
