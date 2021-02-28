import requests
import json

SERVICE_BASE_PATH = "http://test_guild:8080" # Host name is the Container name of the service

def test_given_correct_request__verify_api_is_available():
    r = requests.get(SERVICE_BASE_PATH + "/health")
    assert(r.text == "UP")

def test_given_correct_request__adds_message_to_db():
    message = {
        "sender": "test_user",
        "recipient": "joe",
        "message": "hello world!"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message)
    assert("Message saved" in r.text)

def test_given_malformed_request__returns_400_error():
    message = {
        "sender": "test_user",
        "recipient": "joe"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message)
    assert(r.status_code == 400)

def test_given_two_messages_sent__receives_two_messages_by_sender():
    message_one = {
        "sender": "test_user",
        "recipient": "joe",
        "message": "hello joe!"
    }
    message_two = {
        "sender": "test_user",
        "recipient": "steve",
        "message": "hello steve!"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message_one)
    assert("Message saved" in r.text)
    r = requests.post(SERVICE_BASE_PATH + "/message", json=message_two)
    assert("Message saved" in r.text)

    r = requests.get(SERVICE_BASE_PATH + "/message")
    print(r.json())