from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
import flask_restless

import logging
db = SQLAlchemy()

def create_app(env=None):
    app = Flask(__name__, instance_relative_config=False)
    app.logger.setLevel(logging.INFO)
    app.logger.info(env)
    app.config.from_object('config.Config')
    app.url_map.strict_slashes = True

    db.init_app(app)

    with app.app_context():
        from . import routes
        app.logger.info("routes imported")

        from . import models
        db.create_all()
        app.logger.info("database initiated!")

        @app.route("/health")
        def health():
            return make_response(
                'UP\n',
                200,
            )

        return app
