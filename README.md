# Flask Contact Blueprint
Flask Blueprint to add a simple contact handler to your Flask application. It allows you to send email via
your webapp.

### How it works
This blueprint works by instantiating a view linked to the **'/'** uri (URL prefixing is recommended, see [this](http://flask.pocoo.org/docs/latest/blueprints/#registering-blueprints)). This view can then receive `POST` data either in form data or json. This data
will then be proxied to a specific email via an email backend (currently supports SMTP or [Amazon SES](https://aws.amazon.com/ses/)).

## Installation
Install using [pip](https://pip.pypa.io/en/stable/installing/)

```bash
pip install flask-contact-blueprint
```

or if you want to install the developpement branch:

```bash
pip install git+git@github.com:ddugue/flask-contact-blueprint.git
```

## Minimal example
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

## Basic usage
Assuming you have the configuration above and that your endpoint would be set at `http://example.com`, you could do the following:
```bash
curl -d "email=customer@email.com&message=Hello!" -X POST http://example.com/
```

This would send the following email to `info@company.com`:
```
From: <noreply@company.com>
To: <info@company.com>
Subject: New message

email: customer@email.com
message: Hello!
```

That's it! There exists multiple configuration you can apply to prevent certain fields to be proxied, to work with CORS or to allow files to be sent. Be sure to read the API guide below.


## API Guide
This blueprint is meant to be highly configureable to allow any flask backend to deploy quickly a working endpoint for contact
forms. The endpoint support `JSON` Ajax calls or `POST` Form with a redirect. Most of the configuration is done through the Email Backend.

### <a name="baseemail"></a>Base Email backends

### SMTP Backend
The SMTP Backend (`flask_contact.backends.SMTPBackend`) is a simple SMTP Backend. It connects securely using python [SMTPLib](https://docs.python.org/3/library/smtplib.html) to any SMTP server to send emails
#### Usage
In addition to the usual backend configuration ([See above](#baseemail)). The following fields need to be configured.

class __SMTPBackend__(*smtp_server*=None, *smtp_user*=None, *smtp_password*=None, *smtp_port*=465)
* Where `smtp_server` is the SMTP server endpoint (i.e https://smtp.gmail.com)
* Where `smtp_user` is the SMTP user to use, normally the email address (i.e mailer@gmail.com)
* Where `smtp_password` is the SMTP password to use to connect with smtp\_user. *Alternatively, you can also set environment variable `SMTP_PASSWORD` to automatically set `smtp_password` to desired value*.
* Where `smtp_port` (default: 465) is the SMTP Port to use.

#### Example
```python
import os
import flask_contact

flask_contact.backends.SMTPBackend(
    to_email="info@company.com",
    from_email="noreply@company.com",
    subject="New message from your website",
    smtp_server="http://smtp.gmail.com",
    smtp_user="mailer@gmail.com",
    smtp_password="confidentialPassword1234",
    smtp_port=465,
)
```
### SES Backend
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
#### Usage
#### Customizing backend
### Blueprint
#### CORS
#### Multiple instance
### Posting data
#### Form
#### JSON

## Contributing

## Licensing
This project is licensed under the BSD License - see the [LICENSE](LICENSE) file for details
