from typing import Optional, Dict, Any, List
from ..db import get_db, oid, utcnow

COLLECTION = "comments"

def list_by_task(task_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    task_oid = oid(task_id)
    out = []
    for d in db[COLLECTION].find({"task_id": task_oid}).sort("created_at", 1):
        d["_id"] = str(d["_id"])
        d["task_id"] = str(d["task_id"])
        out.append(d)
    return out

def create(task_id: str, text: str, author: Optional[str]) -> Dict[str, Any]:
    db = get_db()
    doc = {
        "task_id": oid(task_id),
        "text": text.strip(),
        "author": author.strip() if author else None,
        "created_at": utcnow(),
        "updated_at": utcnow(),
    }
    res = db[COLLECTION].insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    doc["task_id"] = str(doc["task_id"])
    return doc

def update(task_id: str, comment_id: str, payload: Dict[str, Any]):
    db = get_db()
    q = {"_id": oid(comment_id), "task_id": oid(task_id)}
    updates = {}
    if "text" in payload:
        updates["text"] = payload["text"].strip()
    if "author" in payload:
        updates["author"] = payload["author"].strip() if payload["author"] else None
    if not updates:
        return None
    updates["updated_at"] = utcnow()
    new_doc = db[COLLECTION].find_one_and_update(q, {"$set": updates}, return_document=True)
    if not new_doc:
        return None
    new_doc["_id"] = str(new_doc["_id"])
    new_doc["task_id"] = str(new_doc["task_id"])
    return new_doc

def delete(task_id: str, comment_id: str) -> bool:
    db = get_db()
    res = db[COLLECTION].delete_one({"_id": oid(comment_id), "task_id": oid(task_id)})
    return res.deleted_count == 1
