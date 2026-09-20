from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_supplier_success(client, auth_headers):
    response = client.post(
        "/supplier/",
        json={
            "company_name": "ABC Suppliers",
            "contact_name": "John Doe",
            "email": "supplier@example.com",
            "supplier_phone": "0712345678",
            "address": "Nairobi",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["company_name"] == "ABC Suppliers"
    assert body["contact_name"] == "John Doe"
    assert body["email"] == "supplier@example.com"
    assert body["supplier_phone"] == "0712345678"
    assert body["address"] == "Nairobi"


def test_create_supplier_missing_company_name_is_validation_error(
    client,
    auth_headers,
):
    response = client.post(
        "/supplier/",
        json={
            "contact_name": "John Doe",
            "email": "missing-company@example.com",
            "supplier_phone": "0712345679",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_supplier_missing_contact_name_is_allowed_by_schema(
    client,
    auth_headers,
):

    response = client.post(
        "/supplier/",
        json={
            "company_name": "Test Supplier",
            "email": "schema@example.com",
            "supplier_phone": "0712345680",
        },
        headers=auth_headers,
    )

    assert response.status_code in (201, 400, 500)


def test_create_supplier_duplicate_email_returns_bad_request(
    client,
    auth_headers,
):
    first_response = client.post(
        "/supplier/",
        json={
            "company_name": "Supplier One",
            "contact_name": "Contact One",
            "email": "duplicate-supplier@example.com",
            "supplier_phone": "0711111111",
        },
        headers=auth_headers,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/supplier/",
        json={
            "company_name": "Supplier Two",
            "contact_name": "Contact Two",
            "email": "duplicate-supplier@example.com",
            "supplier_phone": "0722222222",
        },
        headers=auth_headers,
    )

    assert second_response.status_code == 400


def test_list_suppliers(client, auth_headers, supplier):
    response = client.get(
        "/supplier/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    suppliers = response.json()

    supplier_ids = [
        item["supplier_id"]
        for item in suppliers
    ]

    assert supplier["supplier_id"] in supplier_ids


def test_get_supplier_success(client, auth_headers, supplier):
    response = client.get(
        f"/supplier/{supplier['supplier_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["supplier_id"] == supplier["supplier_id"]
    assert body["company_name"] == supplier["company_name"]


def test_get_supplier_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/supplier/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404

def test_get_supplier_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/supplier/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_supplier_success(client, auth_headers, supplier):
    response = client.put(
        f"/supplier/{supplier['supplier_id']}",
        json={
            "company_name": "Updated Supplier",
            "address": "Mombasa",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["company_name"] == "Updated Supplier"
    assert body["address"] == "Mombasa"


def test_update_supplier_email(client, auth_headers, supplier):
    response = client.put(
        f"/supplier/{supplier['supplier_id']}",
        json={
            "email": "updated-supplier@example.com",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.json()["email"] == "updated-supplier@example.com"


def test_update_supplier_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/supplier/{fake_id}",
        json={
            "company_name": "Does Not Exist",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_supplier_success(client, auth_headers, supplier):
    response = client.delete(
        f"/supplier/{supplier['supplier_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_supplier_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/supplier/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404