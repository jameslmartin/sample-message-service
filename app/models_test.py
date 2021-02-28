from pytest import fixture
from .models import Message

from datetime import datetime, timezone

@fixture
def message() -> Message:
    return Message(
        sender='test', recipient='test2', message="test test", created=datetime.now(timezone.utc)
    )

def test_Message_create(message: Message):
    assert message

## Would also like to test behavior of using things like emoji/ensure text encodings
## work as well
