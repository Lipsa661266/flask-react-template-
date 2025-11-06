from flask import Flask
from .db import init_db
from .comments.routes import bp as comments_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        MONGO_URI="mongodb://localhost:27017/flask_react_dev",
        DB_NAME="flask_react_dev",
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    init_db(app)
    app.register_blueprint(comments_bp, url_prefix="/api")
    return app
