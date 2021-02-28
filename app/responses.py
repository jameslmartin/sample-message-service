from flask import current_app as app
from flask import make_response

headers = {"Content-Type": "application/json"}

## Most of these responses could be abstracted away/removed
## with usage of a Flask REST API framework

def incorrect_mimetype():
    app.logger.error('Unsupported mimetype sent')
    return make_response(
        'Request mimetype not application/json',
        400,
        headers
    )

def malformed_request():
    return make_response(
        'Malformed request, missing JSON fields required',
        400,
        headers
    )

def created_response(id):
    return make_response(
        'Message saved with id: {0}'.format(id),
        200,
        headers
    )

def messages_response(messages):
    return make_response(
        '{0}'.format(messages),
        200,
        headers
    )