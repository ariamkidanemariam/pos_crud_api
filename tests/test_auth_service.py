import pytest
from fastapi import HTTPException

from app.services.auth_service import authenticate
from app.core.security import create_access_token, decode_access_token


def test_authenticate_success(db_session, test_user):
    result = authenticate(
        db_session,
        test_user["username"],
        test_user["password"],
    )

    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert isinstance(result["access_token"], str)
    assert len(result["access_token"]) > 0


def test_authenticate_wrong_password(db_session, test_user):
    with pytest.raises(HTTPException) as exc:
        authenticate(
            db_session,
            test_user["username"],
            "wrongpassword",
        )

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect username or password"


def test_authenticate_nonexistent_user(db_session):
    with pytest.raises(HTTPException) as exc:
        authenticate(
            db_session,
            "doesnotexist",
            "password123",
        )

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect username or password"


def test_authenticate_token_contains_user_id(db_session, test_user, client, auth_headers):
    result = authenticate(
        db_session,
        test_user["username"],
        test_user["password"],
    )

    token = result["access_token"]
    payload = decode_access_token(token)

    users_response = client.get("/user/", headers=auth_headers)
    assert users_response.status_code == 200

    users = users_response.json()
    user = next(
        user for user in users
        if user["username"] == test_user["username"]
    )

    assert payload["sub"] == user["user_id"]
def test_create_access_token_contains_subject():
    token = create_access_token("12345678-1234-1234-1234-123456789012")

    payload = decode_access_token(token)

    assert payload["sub"] == "12345678-1234-1234-1234-123456789012"


def test_create_access_token_contains_expiration():
    token = create_access_token("12345678-1234-1234-1234-123456789012")

    payload = decode_access_token(token)

    assert "exp" in payload
    assert payload["exp"] is not None