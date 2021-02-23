from . import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sender = db.Column(
        db.String(64),
        index=False,
        nullable=False
    )
    recipient = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    message = db.Column(
        db.String(1024),
        index=False,
        unique=True,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __init__(self, sender, recipient, message, created):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.created = created

    def __repr__(self):
        return '<id {}>'.format(self.id)
