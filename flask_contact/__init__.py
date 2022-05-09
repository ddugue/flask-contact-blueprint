from flask import Blueprint, request, abort, jsonify, redirect
from flask_cors import CORS
from .utils import AllowedList, get_domain

def blueprint(name, email_backend, allowed_origins="*"):
    """ Return a blueprint used to send emails to a single contact email

    Send an email via the email backend. On success, will either return
    success true on a json request or a redirect to the form 'redirect_uri'
    on a POST.
    To avoid XSS, only allow redirect to a domain in allowed domain
    """
    bp = Blueprint(name, __name__)
    CORS(bp, origins=allowed_origins)

    origins = AllowedList(allowed_origins)

    @bp.route('/', methods=["POST"])
    def view():
        kwargs = request.json if request.is_json else request.form.to_dict()
        redirect_uri = kwargs.pop('redirect_uri', request.referrer)
        if not request.is_json and not redirect_uri:
            if not redirect_uri:
                abort(400)
            if get_domain(redirect_uri) not in origins:
                abort(401)

        if email_backend.is_red_herring(kwargs):
            abort(400)

        file = request.files.get('file')
        # We generate and send the email via our email backend
        email_backend.mail(kwargs, file)

        if request.is_json:
            return jsonify(success=True)
        return redirect(redirect_uri)

    return bp
