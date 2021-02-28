from flask_sqlalchemy import SQLAlchemy
from .models import Message
from .service import MessageService

import time

## Would have to patch the database with a Mock
## without dependency injection / test fixture db
def test_create(): 
    pass