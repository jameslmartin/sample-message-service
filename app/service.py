from app import db
from datetime import datetime, timedelta, timezone
from .models import Message

import logging

## Globals being used here with the db connection.
## Would be better to use dependency injection
## framework to better unit test

THIRTY_DAYS_AGO = datetime.now() - timedelta(30)

class MessageService:

    @staticmethod
    def create(request_json):
        logging.info("create!")
        logging.info(request_json)
        new_message = Message(
            sender=request_json['sender'],
            recipient=request_json['recipient'],
            message=request_json['message'],
            created=datetime.now(timezone.utc)
        )
        logging.info(new_message)
        db.session.add(new_message)
        db.session.commit()

        return new_message

    @staticmethod
    def get_conversation(query):
        logging.info(query)
        sender = query.get('sender')
        recipient = query.get('recipient')
        logging.info("get convo!")
        messages = Message.query.filter(
            Message.sender == sender,
            Message.recipient == recipient,
            Message.created > THIRTY_DAYS_AGO
            ).limit(100).all()
        return messages

    @staticmethod
    def get_all(query):
        page = query.get('page', 1)
        messages = Message.query.filter(Message.created > THIRTY_DAYS_AGO).limit(100).all()
        return messages
