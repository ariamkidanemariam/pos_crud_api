from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_success(client, auth_headers):
    response = client.post(
        "/user/",
        json={
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "role": "cashier",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == "newuser"
    assert body["first_name"] == "New"
    assert body["last_name"] == "User"
    assert body["email"] == "newuser@example.com"
    assert body["role"] == "cashier"
    assert body["is_active"] is True
    
    assert "password" not in body
    assert "hashed_password" not in body


def test_create_user_missing_required_field_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/user/",
        json={
            "username": "incompleteuser",
            "first_name": "Incomplete",
            "last_name": "User",
            "email": "incomplete@example.com",
            # password missing
            "role": "cashier",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_user_invalid_role_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/user/",
        json={
            "username": "badrole",
            "first_name": "Bad",
            "last_name": "Role",
            "email": "badrole@example.com",
            "password": "password123",
            "role": "admin",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_user_duplicate_email_returns_bad_request(
    client,
    auth_headers,
):
    first_response = client.post(
        "/user/",
        json={
            "username": "firstuser",
            "first_name": "First",
            "last_name": "User",
            "email": "duplicate@example.com",
            "password": "password123",
            "role": "cashier",
        },
        headers=auth_headers,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/user/",
        json={
            "username": "seconduser",
            "first_name": "Second",
            "last_name": "User",
            "email": "duplicate@example.com",
            "password": "password123",
            "role": "cashier",
        },
        headers=auth_headers,
    )

    assert second_response.status_code == 400


def test_list_users(client, auth_headers, test_user):
    response = client.get(
        "/user/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    users = response.json()

    usernames = [user["username"] for user in users]

    assert test_user["username"] in usernames


def test_get_user_success(client, auth_headers, test_user):
    response = client.get(
        "/user/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    users = response.json()

    created_user = next(
        user
        for user in users
        if user["username"] == test_user["username"]
    )

    user_id = created_user["user_id"]

    response = client.get(
        f"/user/{user_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == user_id
    assert body["username"] == test_user["username"]


def test_get_user_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/user/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_user_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/user/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_user_success(client, auth_headers, test_user):
    users_response = client.get(
        "/user/",
        headers=auth_headers,
    )

    assert users_response.status_code == 200

    users = users_response.json()

    user = next(
        user
        for user in users
        if user["username"] == test_user["username"]
    )

    user_id = user["user_id"]

    response = client.put(
        f"/user/{user_id}",
        json={
            "first_name": "Updated",
            "last_name": "Name",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["first_name"] == "Updated"
    assert body["last_name"] == "Name"


def test_update_user_email(client, auth_headers, test_user):
    users_response = client.get(
        "/user/",
        headers=auth_headers,
    )

    users = users_response.json()

    user = next(
        user
        for user in users
        if user["username"] == test_user["username"]
    )

    user_id = user["user_id"]

    response = client.put(
        f"/user/{user_id}",
        json={
            "email": "updated@example.com",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.json()["email"] == "updated@example.com"


def test_update_user_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/user/{fake_id}",
        json={
            "first_name": "Updated",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_user_success(client, auth_headers):
    response = client.post(
        "/user/",
        json={
            "username": "deleteuser",
            "first_name": "Delete",
            "last_name": "User",
            "email": "delete@example.com",
            "password": "password123",
            "role": "cashier",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    user_id = response.json()["user_id"]

    response = client.delete(
        f"/user/{user_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_user_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/user/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404