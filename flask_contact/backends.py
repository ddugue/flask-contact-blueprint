""" Module that regroups different email backends """
import html
import os
import smtplib
import textwrap
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from .utils import AllowedList, filter_args, filename_ext

class EmailBackend:
    """ Provide an interface to send email """

    def __init__(self, from_email, to_email,
                 subject=None, allowed_fields="*", allow_file=False,
                 red_herring=None):
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
        self.red_herring    = red_herring

    def is_red_herring(self, fields):
        """ Function that returns wether the transaction is a red herring

        It should basically use an 'invisible' field on the frontend that shouldn't be
        populated by bots."""
        if self.red_herring and (fields.get(self.red_herring) or None) is not None:
            return True
        return False

    def get_subject(self, fields):
        """ Return the subject of the email message """
        if self.subject is None:
            return "New message" # default value
        if isinstance(self.subject, str):
            return self.subject
        return html.escape(self.subject(**(filter_args(fields, self.subject))))

    def get_file(self, file):
        """ Proxy to check what to return as a file """
        ext = filename_ext(file.filename) if file else None
        if isinstance(self.allow_file, str):
            # We check if file extension is the same as +allow_file+
            return file if ext == self.allow_file else None
        if hasattr(self.allow_file, '__iter__'):
            # We check if file extension is in allowed +allow_file+
            return file if ext in self.allow_file else None
        return file if self.allow_file else None

    def get_message(self, fields):
        """ Craft a multiline message to be sent via email """
        # We need to escape each line from html tags
        lines = []
        for k, item in self.allowed_fields.filter(fields):
            if item:
                lines.append("%s: %s" % (k, item))
        return html.escape('\n'.join(lines))

    def get_reply_email(self, fields):
        """ Return a reply email to be included in email """
        return fields.get('email')

    def get_mail(self, fields, file=None):
        """ Return a Mimetype message """
        message = MIMEMultipart()
        message['Subject'] = self.get_subject(fields)
        message['From'] = self.from_email
        message['To'] = self.to_email

        # We add a reply-to email if there is en email field sent
        reply_email = self.get_reply_email(fields)
        if reply_email:
            message.add_header('reply-to', reply_email)

        # We add the body of the text
        part = MIMEText(self.get_message(fields), 'plain')
        message.attach(part)

        # We add the attachment, if present
        attachment = self.get_file(file)
        if attachment:
            part = MIMEApplication(attachment.read())
            part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            message.attach(part)

        return message

    def mail(self, fields, file=None):
        """ Generate and send an email based on fields passed """
        raise NotImplementedError()

class SMTPEmailBackend(EmailBackend):
    """ Provide an SMTP interface to send email """

    MISSING_SERVER = textwrap.dedent("""
    You need to provide 'smtp_server' value (normally smtp.yourdomain.com) for
    the SMTPEmailBackend to work. """)
    MISSING_USER = textwrap.dedent("""
    You need to provide 'smtp_user' value (normally user@yourdomain.com) for
    the SMTPEmailBackend to work. """)
    MISSING_PASS = textwrap.dedent("""
    You need to provide 'smtp_password' or environment variable SMTP_PASSWORD
    for the SMTPEmailBackend to work. """)

    def __init__(self, *args, smtp_server=None, smtp_user=None,
                 smtp_password=None, smtp_port=465, **kwargs):
        super().__init__(*args, **kwargs)

        self.smtp_server   = smtp_server
        self.smtp_user     = smtp_user
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        self.smtp_port     = smtp_port

        assert self.smtp_server, self.MISSING_SERVER
        assert self.smtp_user, self.MISSING_USER
        assert self.smtp_password, self.MISSING_PASS


    def mail(self, fields, file=None):
        """ We use SMTP to send an email """
        message = self.get_mail(fields, file=None)
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(message['From'], message['To'], message.as_string())
            server.close()
        except smtplib.SMTPAuthenticationError:
            print("The username and/or password you entered is incorrect")
            raise

class SESEmailBackend(EmailBackend):
    """ Provide an interface for SES to send email """

    MISSING_CREDENTIALS = textwrap.dedent("""
    Please provide AWS valid email credentials for the SES Email backend to work
    * You can provide the access key via the access_key parameter in the
    SESEmailBackend constructor or via AWS_ACCESS_KEY_ID_EMAIL environment variable
    * You can provide the secret key via the secret_key parameter in the
    SESEmailBackend constructor or via AWS_SECRET_ACCESS_KEY_EMAIL environment variable
    """)

    def __init__(self, *args, access_key=None, secret_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        import boto3
        access_key = access_key or os.getenv('AWS_ACCESS_KEY_ID_EMAIL')
        secret_key = secret_key or os.getenv('AWS_SECRET_ACCESS_KEY_EMAIL')

        assert access_key, self.MISSING_CREDENTIALS
        assert secret_key, self.MISSING_CREDENTIALS

        self.client = boto3.client(
            'ses',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key or os.getenv('AWS_SECRET_ACCESS_KEY_EMAIL'),
        )


    def mail(self, fields, file=None):
        """ We use boto3 to send email """
        message = self.get_mail(fields, file)

        # We need to send raw email, otherwise file is not supported
        self.client.send_raw_email(
            Source=message['From'],
            Destinations=[message['To']],
            RawMessage={
                'Data': message.as_string()
            }
        )
