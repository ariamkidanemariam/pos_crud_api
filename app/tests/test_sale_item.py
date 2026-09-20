from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_sale_item_success(
    client,
    auth_headers,
    sale,
    product,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 2,
            "unit_price": "1.50",
            "discount_amount": "0.00",
            "total_price": "3.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["sale_id"] == sale["sale_id"]
    assert body["product_id"] == product["product_id"]
    assert body["quantity"] == 2
    assert body["unit_price"] == "1.50"
    assert body["total_price"] == "3.00"


def test_create_sale_item_without_optional_discount(
    client,
    auth_headers,
    sale,
    product,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 1,
            "unit_price": "2.00",
            "total_price": "2.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["quantity"] == 1
    assert body["unit_price"] == "2.00"
    assert body["total_price"] == "2.00"


def test_create_sale_item_missing_required_field_is_validation_error(
    client,
    auth_headers,
    sale,
    product,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 2,
            "unit_price": "1.50",
            # total_price missing
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_sale_item_invalid_sale_id_is_validation_error(
    client,
    auth_headers,
    product,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": "not-a-uuid",
            "product_id": product["product_id"],
            "quantity": 2,
            "unit_price": "1.50",
            "total_price": "3.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_sale_item_invalid_product_id_is_validation_error(
    client,
    auth_headers,
    sale,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": "not-a-uuid",
            "quantity": 2,
            "unit_price": "1.50",
            "total_price": "3.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_sale_item_invalid_quantity_is_validation_error(
    client,
    auth_headers,
    sale,
    product,
):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": "not-a-number",
            "unit_price": "1.50",
            "total_price": "3.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_sale_items(
    client,
    auth_headers,
    sale_item,
):
    response = client.get(
        "/sale-item/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    sale_items = response.json()

    sale_item_ids = [
        item["sale_item_id"]
        for item in sale_items
    ]

    assert sale_item["sale_item_id"] in sale_item_ids


def test_get_sale_item_success(
    client,
    auth_headers,
    sale_item,
):
    response = client.get(
        f"/sale-item/{sale_item['sale_item_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["sale_item_id"] == sale_item["sale_item_id"]
    assert body["sale_id"] == sale_item["sale_id"]
    assert body["product_id"] == sale_item["product_id"]


def test_get_sale_item_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/sale-item/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_sale_item_malformed_uuid_is_validation_error(
    client,
    auth_headers,
):
    response = client.get(
        "/sale-item/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_sale_item_success(
    client,
    auth_headers,
    sale_item,
):
    response = client.put(
        f"/sale-item/{sale_item['sale_item_id']}",
        json={
            "quantity": 5,
            "unit_price": "2.00",
            "total_price": "10.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["quantity"] == 5
    assert body["unit_price"] == "2.00"
    assert body["total_price"] == "10.00"


def test_update_sale_item_quantity(
    client,
    auth_headers,
    sale_item,
):
    response = client.put(
        f"/sale-item/{sale_item['sale_item_id']}",
        json={
            "quantity": 10,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 10


def test_update_sale_item_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.put(
        f"/sale-item/{fake_id}",
        json={
            "quantity": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_delete_sale_item_success(
    client,
    auth_headers,
    sale_item,
):
    response = client.delete(
        f"/sale-item/{sale_item['sale_item_id']}",
        headers=auth_headers,
    )

    assert response.status_code == 204


def test_delete_sale_item_not_found(
    client,
    auth_headers,
):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(
        f"/sale-item/{fake_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404