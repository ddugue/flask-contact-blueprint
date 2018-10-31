from .utils import AllowedList, get_domain
from flask import Blueprint, request, abort, jsonify, redirect

def blueprint(email_backend, allowed_origins="*"):
    """ Return a blueprint used to send emails to a single contact email

    Send an email via the email backend. On success, will either return
    success true on a json request or a redirect to the form 'redirect_uri'
    on a POST.
    To avoid XSS, only allow redirect to a domain in allowed domain
    """
    bp = Blueprint('contact', __name__)
    origins = AllowedList(allowed_origins)

    @bp.route('/', methods="POST")
    def view():
        kwargs = request.json() if request.is_json else request.form.to_dict()
        redirect_uri = kwargs.pop('redirect_uri', request.referrer)
        file = request.files.get('file')

        if not request.is_json and get_domain(redirect_uri) not in origins:
            abort(401)

        # We generate and send the email via our email backend
        email_backend.mail(kwargs, file)

        if request.is_json:
            return jsonify(success=True)
        return redirect(redirect_uri)

    return bp
