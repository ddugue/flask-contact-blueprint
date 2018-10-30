from flask import Blueprint, request, abort, jsonify, redirect

def send_email(from_email, to_email, subject, message, html_message):
    pass

def craft_message(message, **kmwargs):
    pass

def blueprint(from_email, to_email, allow_all=False, allow_file=False,
              allowed_origins="*"):
    """ Return a blueprint used to send emails to a single contact email

    Send an email from +from_email+ to +to_email+, from email is generally a
    no-reply kind of email.

    Optional arguments:
    * allow_all (default: False)   - will include all form fields in the email
    * allow_file (default: False)  - will include a file if a file is present in the request,
                                     if it is a string, only consider files whose
                                     extensions are that string.
    * allowed_origins (default: *) - will allow CORS request from that origin
                                     and will only allow redirect in those domains
                                     (if a list). * means allow all.
    """
    bp = Blueprint('contact', __name__)

    @bp.route('/', methods="POST")
    def view():
        if request.is_json:
            return jsonify(success=True)
        else:
            redirect_uri = request.form.get('redirect_uri') or request.referrer
            if allowed_origins != "*" and redirect_uri not in allowed_origins:
                abort(401)

            message = request.form.get('message', '')
            kwargs = request.form.to_dict()
            return redirect(redirect_uri)

    return bp
