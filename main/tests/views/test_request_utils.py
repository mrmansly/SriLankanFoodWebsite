from django.test import  TestCase
from unittest.mock import MagicMock
from main.views.request_utils import get_session_id


class RequestUtilsTest(TestCase):

    def test_get_session_id_existing_session(self):
        # Mock request with an existing session
        request = MagicMock()
        request.session.session_key = 'existing_session_key'

        session_id = get_session_id(request)
        self.assertEqual(session_id, 'existing_session_key')
        request.session.create.assert_not_called()  # Ensure create is not called

    def test_get_session_id_no_session(self):
        # Mock request with no existing session
        request = MagicMock()
        request.session.session_key = None
        request.session.create = MagicMock()  # Mock create method

        get_session_id(request)

        request.session.create.assert_called_once()  # Ensure create is called

