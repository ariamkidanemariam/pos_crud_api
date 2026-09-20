from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_customer_success(
    client,
    auth_headers,
):
    response = client.post(
        "/customer/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "phone_no": "0712345678",
            "address": "Nairobi",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"
    assert body["phone_no"] == "0712345678"
    assert body["address"] == "Nairobi"
    assert body["is_active"] is True

    assert "customer_id" in body


def test_create_customer_without_optional_fields(
    client,
    auth_headers,
):
    response = client.post(
        "/customer/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["first_name"] == "Jane"
    assert body["last_name"] == "Doe"


def test_create_customer_missing_first_name_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/customer/",
        json={
            "last_name": "Doe",
            "phone_no": "0712345678",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_customer_missing_last_name_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/customer/",
        json={
            "first_name": "John",
            "phone_no": "0712345678",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_customers(
    client,
    auth_headers,
    customer,
):
    response = client.get(
        "/customer/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    customers = response.json()

    customer_ids = [
        item["customer_id"]
        for item in customers
    ]

    assert customer["customer_id"] in customer_ids


def test_get_customer_success(
    client,
    auth_headers,
    customer,
):
    response = client.get(
        f"/customer/{customer['customer_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["customer_id"] == customer["customer_id"]
    assert body["first_name"] == customer["first_name"]
    assert body["last_name"] == customer["last_name"]


def test_get_customer_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/customer/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_customer_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/customer/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_customer_success(
    client,
    auth_headers,
    customer,
):
    response = client.put(
        f"/customer/{customer['customer_id']}",
        json={
            "first_name": "Updated",
            "last_name": "Customer",
            "phone_no": "0799999999",
            "address": "Mombasa",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["first_name"] == "Updated"
    assert body["last_name"] == "Customer"
    assert body["phone_no"] == "0799999999"
    assert body["address"] == "Mombasa"


def test_update_customer_phone_number(
    client,
    auth_headers,
    customer,
):
    response = client.put(
        f"/customer/{customer['customer_id']}",
        json={
            "phone_no": "0700000000",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["phone_no"] == "0700000000"


def test_update_customer_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/customer/{fake_id}",
        json={
            "first_name": "Does",
            "last_name": "Not Exist",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_customer_success(
    client,
    auth_headers,
    customer,
):
    response = client.delete(
        f"/customer/{customer['customer_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_customer_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/customer/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404