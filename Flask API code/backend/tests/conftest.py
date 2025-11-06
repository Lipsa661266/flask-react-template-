import pytest
from backend.app import create_app
from pymongo import MongoClient

@pytest.fixture(scope="session")
def app():
    app = create_app({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/flask_react_test",
        "DB_NAME": "flask_react_test",
    })
    yield app
    MongoClient("mongodb://localhost:27017/").drop_database("flask_react_test")

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def mongo(app):
    from backend.app.db import get_db
    with app.app_context():
        yield get_db()

@pytest.fixture()
def seed_task(mongo):
    doc = {"title": "Test task"}
    inserted = mongo.tasks.insert_one(doc)
    return str(inserted.inserted_id)
