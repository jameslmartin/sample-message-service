import requests
import json

SERVICE_BASE_PATH = "http://localhost:8080"

def test_given_correct_request__verify_api_is_available():
    r = requests.get(SERVICE_BASE_PATH + "/health")
    assert(r.text == "UP")

def test_given_correct_request__adds_message_to_db():
    message = {
        "sender": "james",
        "recipient": "joe",
        "message": "hello world!"
    }
    r = requests.post(SERVICE_BASE_PATH + "/message", data=message)
    print(r.text)

def test_given_malformed_request__returns_400_error():
    pass

def test_given_malformed_request__returns_400_error():
    pass

def test_given_correct_request_with_emoji__adds_message_to_db():
    pass