from flask_sqlalchemy import SQLAlchemy
from .models import Message
from .service import MessageService

import time

## Would have to patch the database with a Mock
## without dependency injection / test fixture db
## then make sure the db.session functions get called
def test_create(): 
    pass

def test_get_conversation():
    pass

def test_get_all():
    pass