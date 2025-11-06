def test_comments_crud_flow(client, seed_task):
    task_id = seed_task

    # list
    res = client.get(f"/api/tasks/{task_id}/comments")
    assert res.status_code == 200
    assert res.get_json() == []

    # create
    payload = {"text": "New comment", "author": "Lipsa"}
    res = client.post(f"/api/tasks/{task_id}/comments", json=payload)
    assert res.status_code == 201
    comment = res.get_json()
    cid = comment["_id"]

    # update
    res = client.patch(f"/api/tasks/{task_id}/comments/{cid}", json={"text": "Edited"})
    assert res.status_code == 200
    assert res.get_json()["text"] == "Edited"

    # delete
    res = client.delete(f"/api/tasks/{task_id}/comments/{cid}")
    assert res.status_code == 204
