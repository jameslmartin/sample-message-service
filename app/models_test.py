from pytest import fixture
from .models import Message

import time

@fixture
def message() -> Message:
    return Message(
        sender='test', recipient='test2', message="test test", created=time.time()*1000
    )

def test_Message_create(message: Message):
    assert message