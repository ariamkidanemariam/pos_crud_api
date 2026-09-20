from urllib import response

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

from datetime import datetime, timezone


def get_test_user_id(client, auth_headers, username):
    response = client.get(
        "/user/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    users = response.json()

    user = next(
        user
        for user in users
        if user["username"] == username
    )

    return user["user_id"]


def test_create_sale_success(
    client,
    auth_headers,
    test_user,
    customer,
):
    user_id = get_test_user_id(
        client,
        auth_headers,
        test_user["username"],
    )

    response = client.post(
        "/sale/",
        json={
            "customer_id": customer["customer_id"],
            "user_id": user_id,
            "sale_date": datetime.now(timezone.utc).isoformat(),
            "subtotal": "10.00",
            "tax_amount": "1.60",
            "discount_amount": "0.00",
            "total_amount": "11.60",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["customer_id"] == customer["customer_id"]
    assert body["user_id"] == user_id
    assert body["subtotal"] == "10.00"
    assert body["tax_amount"] == "1.60"
    assert body["total_amount"] == "11.60"
    assert body["status"] == "completed"


def test_create_sale_missing_required_field_is_validation_error(
    client,
    auth_headers,
    test_user,
    customer,
):
    user_id = get_test_user_id(
        client,
        auth_headers,
        test_user["username"],
    )

    response = client.post(
        "/sale/",
        json={
            "customer_id": customer["customer_id"],
            "user_id": user_id,
            "sale_date": datetime.now(timezone.utc).isoformat(),
            "subtotal": "10.00",
            "tax_amount": "1.60",
            # total_amount missing
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_sale_invalid_customer_uuid_is_validation_error(
    client,
    auth_headers,
    test_user,
):
    user_id = get_test_user_id(
        client,
        auth_headers,
        test_user["username"],
    )

    response = client.post(
        "/sale/",
        json={
            "customer_id": "not-a-uuid",
            "user_id": user_id,
            "sale_date": datetime.now(timezone.utc).isoformat(),
            "subtotal": "10.00",
            "tax_amount": "1.60",
            "total_amount": "11.60",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_sale_invalid_status_is_validation_error(
    client,
    auth_headers,
    test_user,
    customer,
):
    user_id = get_test_user_id(
        client,
        auth_headers,
        test_user["username"],
    )

    response = client.post(
        "/sale/",
        json={
            "customer_id": customer["customer_id"],
            "user_id": user_id,
            "sale_date": datetime.now(timezone.utc).isoformat(),
            "subtotal": "10.00",
            "tax_amount": "1.60",
            "total_amount": "11.60",
            "status": "invalid_status",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_sales(
    client,
    auth_headers,
    sale,
):
    response = client.get(
        "/sale/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    sales = response.json()

    sale_ids = [
        item["sale_id"]
        for item in sales
    ]

    assert sale["sale_id"] in sale_ids


def test_get_sale_success(
    client,
    auth_headers,
    sale,
):
    response = client.get(
        f"/sale/{sale['sale_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["sale_id"] == sale["sale_id"]


def test_get_sale_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/sale/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_sale_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/sale/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_sale_success(
    client,
    auth_headers,
    sale,
):
    response = client.put(
        f"/sale/{sale['sale_id']}",
        json={
            "customer_id": sale["customer_id"],
            "user_id": sale["user_id"],
            "subtotal": "20.00",
            "tax_amount": "3.20",
            "total_amount": "23.20",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["subtotal"] == "20.00"
    assert body["tax_amount"] == "3.20"
    assert body["total_amount"] == "23.20"


def test_update_sale_status(
    client,
    auth_headers,
    sale,
):
    response = client.put(
        f"/sale/{sale['sale_id']}",
        json={
            "customer_id": sale["customer_id"],
            "user_id": sale["user_id"],
            "status": "cancelled",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.json()["status"] == "cancelled"


def test_update_sale_not_found(
    client,
    auth_headers,
    test_user,
    customer,
):
    user_id = get_test_user_id(
        client,
        auth_headers,
        test_user["username"],
    )

    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/sale/{fake_id}",
        json={
            "customer_id": customer["customer_id"],
            "user_id": user_id,
            "subtotal": "20.00",
            "tax_amount": "3.20",
            "total_amount": "23.20",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
def test_delete_sale_success(
    client,
    auth_headers,
    sale,
):
    response = client.delete(
        f"/sale/{sale['sale_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_sale_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/sale/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404