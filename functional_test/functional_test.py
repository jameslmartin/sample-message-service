import requests
import json

import uuid

# Host name is the Container name of the service, this hard coded URL
# assumes the service is available at guild:8080 (run with Docker compose and
# functional tests are on the `guild` Docker network)
SERVICE_BASE_PATH = "http://guild:8080"

def test_given_correct_request__verify_api_is_available():
    r = requests.get(SERVICE_BASE_PATH + "/health")
    assert(r.text == "UP\n")

def test_given_correct_request__adds_message_to_db():
    message = {
        "sender": "test_user",
        "recipient": "joe",
        "message": "hello world!"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message)
    assert("Message saved" in r.text)
    assert(r.status_code == 200)

def test_given_malformed_request__returns_400_error():
    message = {
        "sender": "test_user",
        "recipient": "joe"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message)
    assert(r.status_code == 400)

def test_given_two_messages_sent__receives_two_messages_by_sender():
    id = str(uuid.uuid4())
    message_one = {
        "sender": "test_user",
        "recipient": id,
        "message": "hello test user!"
    }
    message_two = {
        "sender": "test_user",
        "recipient": id,
        "message": "hello test user!"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message_one)
    assert("Message saved" in r.text)
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message_two)
    assert("Message saved" in r.text)

    r = requests.get(SERVICE_BASE_PATH + "/message?sender=test_user&recipient={0}".format(id))
    assert(len(r.json()) == 2)
