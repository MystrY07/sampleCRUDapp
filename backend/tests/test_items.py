# CREATE


def test_create_item(client):
    response = client.post(
        "/items/",
        json={"name": "Widget", "description": "A useful widget"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Widget"
    assert data["description"] == "A useful widget"
    assert "id" in data


def test_create_item_without_description(client):
    response = client.post("/items/", json={"name": "Bare item"})
    assert response.status_code == 200
    assert response.json()["description"] is None


def test_create_item_duplicate_name(client):
    client.post("/items/", json={"name": "Widget"})
    response = client.post("/items/", json={"name": "Widget"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


# READ


def test_read_items_empty(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_items(client):
    client.post("/items/", json={"name": "First"})
    client.post("/items/", json={"name": "Second"})
    response = client.get("/items/")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["First", "Second"]


def test_read_items_skip_limit(client):
    for i in range(5):
        client.post("/items/", json={"name": f"Item {i}"})
    response = client.get("/items/", params={"skip": 2, "limit": 2})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_item(client):
    created = client.post("/items/", json={"name": "Solo"}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Solo"


def test_read_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


# UPDATE


def test_update_item(client):
    created = client.post("/items/", json={"name": "Old"}).json()
    response = client.put(
        f"/items/{created['id']}",
        json={"name": "New", "description": "Updated"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New"
    assert data["description"] == "Updated"
    assert data["id"] == created["id"]


def test_update_item_not_found(client):
    response = client.put("/items/999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_update_item_duplicate_name(client):
    client.post("/items/", json={"name": "Taken"})
    created = client.post("/items/", json={"name": "Other"}).json()
    response = client.put(
        f"/items/{created['id']}", json={"name": "Taken"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


# DELETE


def test_delete_item(client):
    created = client.post("/items/", json={"name": "Doomed"}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
