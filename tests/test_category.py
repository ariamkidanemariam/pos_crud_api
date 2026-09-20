from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_category_success(
    client,
    auth_headers,
):
    response = client.post(
        "/category/",
        json={
            "name": "Beverages",
            "description": "Drinks and beverages",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Beverages"
    assert body["description"] == "Drinks and beverages"
    assert body["is_active"] is True
    assert "category_id" in body


def test_create_category_without_optional_fields(
    client,
    auth_headers,
):
    response = client.post(
        "/category/",
        json={
            "name": "Snacks",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Snacks"


def test_create_category_missing_name_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/category/",
        json={
            "description": "Category without a name",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_category_empty_body_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/category/",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_categories(
    client,
    auth_headers,
    category,
):
    response = client.get(
        "/category/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    categories = response.json()

    category_ids = [
        item["category_id"]
        for item in categories
    ]

    assert category["category_id"] in category_ids


def test_get_category_success(
    client,
    auth_headers,
    category,
):
    response = client.get(
        f"/category/{category['category_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["category_id"] == category["category_id"]
    assert body["name"] == category["name"]


def test_get_category_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/category/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_category_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/category/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_category_success(
    client,
    auth_headers,
    category,
):
    response = client.put(
        f"/category/{category['category_id']}",
        json={
            "name": "Updated Category",
            "description": "Updated description",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Updated Category"
    assert body["description"] == "Updated description"


def test_update_category_name(
    client,
    auth_headers,
    category,
):
    response = client.put(
        f"/category/{category['category_id']}",
        json={
            "name": "Updated Name",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_category_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/category/{fake_id}",
        json={
            "name": "Does Not Exist",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_category_success(
    client,
    auth_headers,
    category,
):
    response = client.delete(
        f"/category/{category['category_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_category_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/category/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404