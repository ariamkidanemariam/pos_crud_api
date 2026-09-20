from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_receipt_success(
    client,
    auth_headers,
    sale,
):
    response = client.post(
    "/receipt/",
    json={
        "sale_id": sale["sale_id"],
        "receipt_number": "REC-0001",
        "receipt_type": "sales_receipt",
        "receipt_data": "Test receipt",
    },
    headers=auth_headers,
)
    assert response.status_code == 201

    body = response.json()

    assert body["sale_id"] == sale["sale_id"]
    assert "receipt_id" in body


def test_create_receipt_missing_sale_id_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/receipt/",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_receipt_invalid_sale_id_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/receipt/",
        json={
            "sale_id": "not-a-uuid",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_receipts(
    client,
    auth_headers,
    receipt,
):
    response = client.get(
        "/receipt/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    receipts = response.json()

    receipt_ids = [
        item["receipt_id"]
        for item in receipts
    ]

    assert receipt["receipt_id"] in receipt_ids


def test_get_receipt_success(
    client,
    auth_headers,
    receipt,
):
    response = client.get(
        f"/receipt/{receipt['receipt_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["receipt_id"] == receipt["receipt_id"]
    assert body["sale_id"] == receipt["sale_id"]


def test_get_receipt_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/receipt/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_receipt_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/receipt/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_receipt_success(
    client,
    auth_headers,
    receipt,
):
    response = client.put(
        f"/receipt/{receipt['receipt_id']}",
        json={
            "sale_id": receipt["sale_id"],
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["receipt_id"] == receipt["receipt_id"]


def test_update_receipt_not_found(
    client,
    auth_headers,
    sale,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/receipt/{fake_id}",
        json={
            "sale_id": sale["sale_id"],
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_receipt_success(
    client,
    auth_headers,
    receipt,
):
    response = client.delete(
        f"/receipt/{receipt['receipt_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_receipt_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/receipt/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404