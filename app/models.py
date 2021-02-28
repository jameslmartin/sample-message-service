from app import db
from sqlalchemy.dialects.postgresql import UUID

import json
import uuid

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    sender = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    recipient = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    message = db.Column(
        db.String(1024),
        index=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __init__(self, sender, recipient, message, created):
        self.id = uuid.uuid4()
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.created = created

    ## Limited to this representation of the model 
    def __repr__(self):
        return json.dumps({ 
            'sender': self.sender,
            'recipient': self.recipient,
            'message': self.message
        })
