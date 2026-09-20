from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product_success(client, auth_headers, category, supplier):
    response = client.post(
        "/product/",
        json={
            "name": "Pepsi 330ml",
            "price": "1.25",
            "quantity": 50,
            "category_id": category["category_id"],
            "supplier_id": supplier["supplier_id"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Pepsi 330ml"
    assert body["is_active"] is True


def test_create_product_without_category_or_supplier_is_allowed(client, auth_headers):
    response = client.post(
        "/product/",
        json={"name": "Generic Item", "price": "0.99", "quantity": 10},
        headers=auth_headers,
    )
    assert response.status_code == 201


def test_create_product_missing_required_field_is_a_validation_error(
    client, auth_headers
):
    response = client.post(
        "/product/", json={"name": "No price or quantity"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_create_product_malformed_category_id_is_a_validation_error(
    client, auth_headers
):
    response = client.post(
        "/product/",
        json={
            "name": "Bad FK",
            "price": "1.00",
            "quantity": 1,
            "category_id": "not-a-uuid",
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_list_products(client, auth_headers, product):
    response = client.get("/product/", headers=auth_headers)
    assert response.status_code == 200
    ids = [p["product_id"] for p in response.json()]
    assert product["product_id"] in ids


def test_get_product_not_found(client, auth_headers):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/product/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


def test_update_product(client, auth_headers, product):
    response = client.put(
        f"/product/{product['product_id']}",
        json={"price": "2.00", "quantity": 5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["quantity"] == 5


def test_update_product_with_uuid_fk_change(client, auth_headers, product, category):
    response = client.put(
        f"/product/{product['product_id']}",
        json={"category_id": category["category_id"]},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["category_id"] == category["category_id"]


def test_delete_product_as_manager_succeeds(client, auth_headers, product):
    response = client.delete(
        f"/product/{product['product_id']}", headers=auth_headers
    )
    assert response.status_code == 204


def test_delete_product_as_cashier_is_forbidden(client, cashier_auth_header, product):
    response = client.delete(
        f"/product/{product['product_id']}", headers=cashier_auth_header
    )
    assert response.status_code == 403