""" Module that regroups different email backends """
import html
import os

from .utils import AllowedList, filter_args

class EmailBackend:
    """ Provide an interface to send email """

    def __init__(self, from_email, to_email,
                 subject=None, allowed_fields="*", allow_file=False):
        """ Configuration for email backend:

        * from_email: Email address to send emails from
        * to_email:   Email address to send email to
        * subject_fn: Lambda that generate the subject of the message
        * allowed_fields: Fields that will be included in the message
        * allow_file: Allow files to be joined to the email
        """
        self.from_email     = from_email
        self.to_email       = to_email
        self.subject        = subject
        self.allowed_fields = AllowedList(allowed_fields)
        self.allow_file     = allow_file

    def get_subject(self, fields):
        """ Return the subject of the email message """
        if self.subject is None:
            return "New message" # default value
        if isinstance(self.subject, str):
            return self.subject
        return html.escape(self.subject(**(filter_args(fields, self.subject))))

    def get_file(self, file):
        """ Proyx to check what to return as a file """
        return file if self.allow_file else None

    def get_message(self, fields):
        """ Craft a multiline message to be sent via email """
        # We need to escape each line from html tags
        lines = []
        for k, item in self.allowed_fields.filter(fields):
            lines.append("%s: %s" % (k, item))
        return html.escape('\n'.join(lines))

    def mail(self, fields, file=None):
        """ Generate and send an email based on fields passed """
        raise NotImplementedError()

class SESEmailBackend(EmailBackend):
    """ Provide an interface for SES to send email """

    def __init__(self, *args, access_key=None, secret_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        import boto3
        self.client = boto3.client(
            'ses',
            aws_access_key_id=access_key or os.getenv('AWS_ACCESS_KEY_ID_EMAIL'),
            aws_secret_access_key=secret_key or os.getenv('AWS_SECRET_ACCESS_KEY_EMAIL'),
        )

    def get_reply_email(self, fields):
        """ Return a reply email to be included in email """
        return fields.get('email')

    def mail(self, fields, file=None):
        kwargs = {
            "Source": self.from_email,
            "Destination": {
                'ToAddresses': [
                    self.to_email,
                ],
            },
            "Message": {
                'Subject': {
                    'Data': self.get_subject(fields),
                },
                'Body': {
                    'Text': {
                        'Data': self.get_message(fields),
                    },
                }
            },
        }
        reply_email = self.get_reply_email(fields)
        if reply_email:
            kwargs["ReplyToAddresses"] = [reply_email]
        self.client.send_email(**kwargs)
