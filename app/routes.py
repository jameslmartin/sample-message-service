from flask import current_app as app
from flask import request
from .models import Message
from .responses import incorrect_mimetype, malformed_request, created_response, messages_response
from .service import MessageService

import json
import time

headers = {"Content-Type": "application/json"}

@app.route("/message", methods=['POST', 'GET'])
def message():
    response = ""
    if request.method == 'POST':
        if request.is_json:
            if has_required_fields(request):
                new_message = MessageService.create(request.json)
                response = created_response(new_message.id)
            else:
                response = malformed_request()
        else:
            response = incorrect_mimetype()
    
    if request.method == 'GET':
        query = request.args
        messages = MessageService.get_conversation(query) if is_conversation_query(query) \
            else MessageService.get_all(query)
        response = messages_response(messages)
        
    return response

def is_conversation_query(query):
    app.logger.info('query: {0}'.format(query))
    return query.get('sender') and query.get('recipient')

## If other fields are passed, they will just be ignored
## Really want to use an additional Flask library
## to accept/respond with a schema
def has_required_fields(request):
    json = request.json
    app.logger.info(json)
    return \
        json.get('sender') and \
        json.get('recipient') and \
        json.get('message')