from flask import Flask
from flask_contact.backends import SESEmailBackend
from flask_contact import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint('contact', SESEmailBackend(
    'noreply@neosmartblinds.com',
    'ddugue@neosmartblinds.com',
    allowed_fields='email message'
)), url_prefix='/contact')
app.register_blueprint(blueprint('job', SESEmailBackend(
    'noreply@neosmartblinds.com',
    'ddugue@neosmartblinds.com',
    allowed_fields='email position message',
    allow_file=True,
)), url_prefix='/jobs')
