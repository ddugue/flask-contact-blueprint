from flask import Flask
from flask_contact.backends import SESEmailBackend
from flask_contact import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint(SESEmailBackend(
    'noreply@neosmartblinds.com',
    'ddugue@neosmartblinds.com'
)))
