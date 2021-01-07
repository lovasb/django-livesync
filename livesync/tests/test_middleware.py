from unittest import TestCase

from django.template.backends.dummy import Template
from django.test import override_settings
from mock import Mock, PropertyMock, patch
from livesync.core.middleware import DjangoLiveSyncMiddleware


class LiveSyncMiddlewareTestCase(TestCase):
    def setUp(self):
        self.mocked_response = Mock()
        self.get_response = Mock(return_value=self.mocked_response)
        self.middleware = DjangoLiveSyncMiddleware(self.get_response)
        self.mock_content_property = PropertyMock(return_value=b"<body></body>")
        type(self.mocked_response).content = self.mock_content_property

    @override_settings(DEBUG=True)
    def test_middleware_injects_js_file_correctly(self):
        self.mocked_response.__getitem__ = Mock(return_value='text/html')
        # act
        self.middleware(Mock())
        # assert

        self.mock_content_property.assert_called()
        self.assertTrue(b"<script src='/static/livesync.js'></script>" in self.mock_content_property.call_args[0][0])

    @override_settings(DEBUG=True)
    def test_middleware_does_not_inject_js_file_if_content_type_is_not_html(self):
        self.mocked_response.__getitem__ = Mock(return_value='json')
        # act
        self.middleware(Mock())
        # assert
        self.mock_content_property.assert_not_called()

    @override_settings(DEBUG=False)
    def test_middleware_does_not_inject_js_file_if_not_debugging(self):
        self.mocked_response.__getitem__ = Mock(return_value='text/html')
        # act
        self.middleware(Mock())
        # assert
        self.mock_content_property.assert_not_called()

    @override_settings(DEBUG=True)
    @patch('django.template.loader.get_template')
    def test_middleware_custom_snippet_injektion(self, mock_template):
        self.mocked_response.__getitem__ = Mock(return_value='text/html')

        mock_template.return_value = Template('mocked_snippet')
        # act
        self.middleware(Mock())
        # assert

        self.mock_content_property.assert_called()
        self.assertTrue(b"mocked_snippet" in self.mock_content_property.call_args[0][0])
