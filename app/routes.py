from flask import current_app as app
from flask import make_response, request
from .models import Message

import json
import time

headers = {"Content-Type": "application/json"}

@app.route("/message", methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        # print(request.form)
        message = Message(
            sender=request.form['sender'],
            recipient=request.form['recipient'],
            message=request.form['message'],
            created=time.time()*1000 # epoch milli
        )
        print(message)
    return make_response(
        'Messages endpoint hit!',
        200,
        headers
    )