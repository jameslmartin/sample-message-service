from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

db = SQLAlchemy()
print("db initialized")

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes
        print("routes imported")

        from . import models
        db.create_all()
        print("Database initiated!")

        # manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

        # manager.create_api(models.Message, methods=['GET'], url_prefix='/get')
        # manager.create_api(models.Message, methods=['POST'], url_prefix='/add')

        return app
