from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from . import repository as repo
from ..db import oid

bp = Blueprint("comments", __name__)

@bp.get("/tasks/<task_id>/comments")
def list_comments(task_id):
    try:
        oid(task_id)
    except Exception:
        raise BadRequest("Invalid task_id")
    return jsonify(repo.list_by_task(task_id)), 200

@bp.post("/tasks/<task_id>/comments")
def create_comment(task_id):
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if not text:
        raise BadRequest("Missing text field")
    created = repo.create(task_id, text, data.get("author"))
    return jsonify(created), 201

@bp.patch("/tasks/<task_id>/comments/<comment_id>")
def update_comment(task_id, comment_id):
    data = request.get_json(silent=True) or {}
    updated = repo.update(task_id, comment_id, data)
    if not updated:
        raise NotFound("Comment not found or no updates")
    return jsonify(updated), 200

@bp.delete("/tasks/<task_id>/comments/<comment_id>")
def delete_comment(task_id, comment_id):
    if not repo.delete(task_id, comment_id):
        raise NotFound("Comment not found")
    return "", 204
