# Flask Contact Blueprint
Flask Blueprint to add a simple contact handler to your Flask application. It allows you to send email via
your webapp. Support [SES]() and SMTP

## Getting started
In order to getting started, start by installing flask-contact-blueprint

### Installation
Install using [pip]()

```bash
pip install flask-contact-blueprint
```

or if you want to install the developpement branch:

```bash
pip install git+git@github.com:ddugue/flask-contact-blueprint.git
```

### Minimal example
```python
import os
from flask import Flask
from flask_contact import backends, blueprint as contact_blueprint

email_backend = backends.SMTPBackend(
    to_email="info@company.com",
    from_email="noreply@company.com",
    smtp_server="http://smtp.server.com",
    smtp_user="mail-agent",
    smtp_password=os.getenv('CONFIDENTIAL_SMTP_PASSWORD'),
)

app = Flask(__name__)
app.register_blueprint(contact_blueprint(email_backend))
```

### How it works
This blueprint works by instantiating a view linked to the **'/'** uri (URL prefixing is recommended, see [this](http://flask.pocoo.org/docs/latest/blueprints/#registering-blueprints)). This view can then receive POST data either in form data or json. This data
will then be proxied to a specific email.

## API Guide
### Email backends
#### Base Configuration
#### SMTP Backend
#### SES Backend
The SES Backend uses Amazon SES to send email. flask-contact-blueprint uses boto3 to send its email. When
installing make sure to install boto3 with pip if you want to use the SES backend:
```
pip install boto3
```
or alternatively, when installing flask-contact-blueprint:
```
pip install flask-contact-blueprint[ses]
```
this will automatically pull boto3's latest version.
##### Usage
#### Customizing backend
### Blueprint
#### CORS
#### Multiple instance
### Posting data
#### Form
#### JSON
