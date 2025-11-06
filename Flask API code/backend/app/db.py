from flask import current_app, g
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime

def get_db():
    if "db" not in g:
        uri = current_app.config["MONGO_URI"]
        name = current_app.config["DB_NAME"]
        client = MongoClient(uri)
        g._mongo_client = client
        g.db = client[name]
    return g.db

def close_db(e=None):
    client = g.pop("_mongo_client", None)
    if client:
        client.close()

def init_db(app):
    @app.teardown_appcontext
    def teardown(exception):
        close_db()
    with app.app_context():
        db = get_db()
        db.comments.create_index([("task_id", ASCENDING)])
        db.tasks.create_index([("created_at", ASCENDING)])

def oid(value: str):
    try:
        return ObjectId(value)
    except Exception:
        raise ValueError("Invalid ObjectId")

def utcnow():
    return datetime.utcnow()
