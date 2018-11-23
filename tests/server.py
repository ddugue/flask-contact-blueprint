""" This is a test server to run the test """
from flask import Flask
from flask_contact.backends import SESEmailBackend, SMTPEmailBackend
from flask_contact import blueprint

app = Flask(__name__)

# app.register_blueprint(blueprint('job', SESEmailBackend(
#     'noreply@example.com',
#     'target@example.com',
#     allowed_fields='email position message',
#     allow_file=True,
# )), url_prefix='/jobs')

app.register_blueprint(blueprint('smtp', SMTPEmailBackend(
    'from@example.com',
    'to@example.ca',
    smtp_user='from@example.com',
    smtp_server='smtp.gmail.com',
    allowed_fields='email message',
    allow_file=True,
)), url_prefix='/smtp')
