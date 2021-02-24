from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
import flask_restless

db = SQLAlchemy()
print("db initialized")

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.url_map.strict_slashes = True

    db.init_app(app)

    with app.app_context():
        from . import routes
        print("routes imported")

        from . import models
        db.create_all()
        print("database initiated!")

        @app.route("/health")
        def health():
            return make_response(
                'UP',
                200,
            )

        return app
