import unittest
from unittest.mock import MagicMock

from flask_contact.backends import EmailBackend

class EmailFormattingTest(unittest.TestCase):
    """ Test case to test email backend formatting """

    def test_subject_none(self):
        "Test that an empty subject is generated"
        backend = EmailBackend('', '')
        self.assertEqual(backend.get_subject({}), 'New message')

    def test_subject_string(self):
        "Test that a string subject is used"
        backend = EmailBackend('', '', subject="Message")
        self.assertEqual(backend.get_subject({}), 'Message')

    def test_subject_empty_lambda(self):
        "Test that a lambda subject is used"
        backend = EmailBackend('', '', subject=lambda: "Hello")
        self.assertEqual(backend.get_subject({}), 'Hello')

    def test_subject_arg_lambda(self):
        "Test that a lambda subject is used"
        backend = EmailBackend('', '', subject=lambda name='': "Hello " + name)
        self.assertEqual(
            backend.get_subject({'name': 'David', 'other': 'Bam'}),
            'Hello ' + 'David'
        )

    def test_empty_message(self):
        "Test that get message work with an empty message"
        backend = EmailBackend('', '')
        self.assertEqual(backend.get_message({}), '')

    def test_arg_message(self):
        "Test that get message work with an some args"
        backend = EmailBackend('', '')
        self.assertEqual(backend.get_message({'name': 'David'}), 'name: David')

    def test_arg_message(self):
        "Test that get message work with an some args AND a filter"
        backend = EmailBackend('', '', allowed_field='name')
        self.assertEqual(backend.get_message({'name': 'David'}), 'name: David')

    def test_arg_message(self):
        "Test that get message work with an some filter args"
        backend = EmailBackend('', '', allowed_fields='')
        self.assertEqual(backend.get_message({'name': 'David'}), '')

    def test_escape(self):
        "Test that get message escape its args"
        backend = EmailBackend('', '')
        self.assertEqual(backend.get_message({'name': '<a>David</a>'}),
                         'name: &lt;a&gt;David&lt;/a&gt;')

    def test_file_disallow(self):
        "Make sure that when calling send_mail with allow_file False doesnt pass file"
        backend = EmailBackend('', '')
        backend.send_email = MagicMock()
        backend.mail({}, 2)
        backend.send_email.assert_called_with('', '', 'New message', '', None)

    def test_file_allow(self):
        "Make sure that when calling send_mail with allow_file True pass file"
        backend = EmailBackend('', '', allow_file=True)
        backend.send_email = MagicMock()
        backend.mail({}, 2)
        backend.send_email.assert_called_with('', '', 'New message', '', 2)
