from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_payment_success(
    client,
    auth_headers,
    sale,
):
    response = client.post(
        "/payment/",
        json={
            "sale_id": sale["sale_id"],
            "amount": "11.60",
            "payment_method": "cash",
            "status": "completed",
            "payment_date": "2026-09-20T10:00:00Z"
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["sale_id"] == sale["sale_id"]
    assert body["amount"] == "11.60"
    assert body["payment_method"] == "cash"
    assert body["status"] == "completed"
    assert "payment_id" in body


def test_create_payment_missing_required_field_is_validation_error(
    client,
    auth_headers,
    sale,
):
    response = client.post(
        "/payment/",
        json={
            "sale_id": sale["sale_id"],
            # amount missing
            "payment_method": "cash",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_payment_invalid_sale_id_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/payment/",
        json={
            "sale_id": "not-a-uuid",
            "amount": "10.00",
            "payment_method": "cash",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_payment_invalid_payment_method_is_validation_error(
    client,
    auth_headers,
    sale,
):
    response = client.post(
        "/payment/",
        json={
            "sale_id": sale["sale_id"],
            "amount": "10.00",
            "payment_method": "invalid_method",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_payment_invalid_status_is_validation_error(
    client,
    auth_headers,
    sale,
):
    response = client.post(
        "/payment/",
        json={
            "sale_id": sale["sale_id"],
            "amount": "10.00",
            "payment_method": "cash",
            "status": "invalid_status",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_payments(
    client,
    auth_headers,
    payment,
):
    response = client.get(
        "/payment/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    payments = response.json()

    payment_ids = [
        item["payment_id"]
        for item in payments
    ]

    assert payment["payment_id"] in payment_ids


def test_get_payment_success(
    client,
    auth_headers,
    payment,
):
    response = client.get(
        f"/payment/{payment['payment_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["payment_id"] == payment["payment_id"]
    assert body["sale_id"] == payment["sale_id"]


def test_get_payment_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/payment/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_payment_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/payment/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_payment_success(
    client,
    auth_headers,
    payment,
):
    response = client.put(
        f"/payment/{payment['payment_id']}",
        json={
            "amount": "20.00",
            "payment_method": "cash",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["amount"] == "20.00"
    assert body["payment_method"] == "cash"
    assert body["status"] == "completed"


def test_update_payment_status(
    client,
    auth_headers,
    payment,
):
    response = client.put(
        f"/payment/{payment['payment_id']}",
        json={
            "status": "refunded",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.json()["status"] == "refunded"


def test_update_payment_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/payment/{fake_id}",
        json={
            "amount": "20.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_payment_success(
    client,
    auth_headers,
    payment,
):
    response = client.delete(
        f"/payment/{payment['payment_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_payment_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/payment/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404