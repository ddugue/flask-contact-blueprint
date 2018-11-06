from flask import Flask
from flask_contact.backends import SESEmailBackend, SMTPEmailBackend
from flask_contact import blueprint

app = Flask(__name__)

# app.register_blueprint(blueprint('contact', SESEmailBackend(
#     'noreply@neosmartblinds.com',
#     'ddugue@neosmartblinds.com',
#     allowed_fields='email message'
# )), url_prefix='/contact')

# app.register_blueprint(blueprint('job', SESEmailBackend(
#     'noreply@neosmartblinds.com',
#     'ddugue@neosmartblinds.com',
#     allowed_fields='email position message',
#     allow_file=True,
# )), url_prefix='/jobs')

app.register_blueprint(blueprint('smtp', SMTPEmailBackend(
    'ddugue@neosmartblinds.com',
    'ddugue@kumoweb.ca',
    smtp_user='ddugue@neosmartblinds.com',
    smtp_server='smtp.gmail.com',
    allowed_fields='email message',
    allow_file=True,
)), url_prefix='/smtp')
