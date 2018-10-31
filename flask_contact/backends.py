""" Module that regroups different email backends """
import html

from utils import AllowedList, filter_args

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
        return self.subject(**(filter_args(fields, self.subject)))

    def get_message(self, fields):
        """ Craft a multiline message to be sent via email """
        # We need to escape each line from html tags
        lines = []
        for k, item in self.allowed_fields.filter(fields):
            lines.append("%s: %s" % (html.escape(k), html.escape(item)))
        return '\n'.join(lines)

    @staticmethod
    def send_email(from_email, to_email, subject, message, file=None):
        """ Actually send an email via the current backend """
        pass

    def mail(self, fields, file=None):
        """ Generate and send an email based on fields passed """
        self.send_email(
            self.from_email,
            self.to_email,
            self.get_subject(fields),
            self.get_message(fields),
            file if self.allow_file else None,
        )
