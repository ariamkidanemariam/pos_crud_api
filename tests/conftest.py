import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "store_manager",
        "is_active": True,
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201, (
        f"Registration failed: {response.text}"
    )

    return user_data

@pytest.fixture
def manager_user(client):
    user_data = {
        "username": "manager",
        "first_name": "Store",
        "last_name": "Manager",
        "email": "manager@example.com",
        "password": "managerpass123",
        "role": "store_manager",
        "is_active": True,
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 201, (
        f"Manager registration failed: {response.text}"
    )

    return user_data

@pytest.fixture
def cashier_user(client):
    user_data = {
        "username": "cashier",
        "first_name": "Test",
        "last_name": "Cashier",
        "email": "cashier@example.com",
        "password": "cashierpass123",
        "role": "cashier",
        "is_active": True,
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 201, (
        f"Cashier registration failed: {response.text}"
    )

    return user_data


@pytest.fixture
def auth_header(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )

    assert response.status_code == 200, (
        f"Login failed: {response.text}"
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def manager_auth_header(client, manager_user):
    response = client.post(
        "/auth/login",
        data={
            "username": manager_user["username"],
            "password": manager_user["password"],
        },
    )

    assert response.status_code == 200, (
        f"Manager login failed: {response.text}"
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def cashier_auth_header(client, cashier_user):
    response = client.post(
        "/auth/login",
        data={
            "username": cashier_user["username"],
            "password": cashier_user["password"],
        },
    )

    assert response.status_code == 200, (
        f"Cashier login failed: {response.text}"
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def auth_headers(auth_header):
    return auth_header
@pytest.fixture
def product(client, auth_headers):
    response = client.post(
        "/product/",
        json={
            "name": "Test Product",
            "price": "10.00",
            "quantity": 100,
            "barcode": "TEST-001",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Product creation failed: {response.text}"
    )

    return response.json()
@pytest.fixture
def sale_item(client, auth_headers, sale, product):
    response = client.post(
        "/sale-item/",
        json={
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": 2,
            "unit_price": "10.00",
            "discount_amount": "0.00",
            "total_price": "20.00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Sale item creation failed: {response.text}"
    )

    return response.json()

@pytest.fixture
def category(client, auth_headers):
    response = client.post(
        "/category/",
        json={
            "name": "Beverages",
            "description": "Drinks and beverages",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Category creation failed: {response.text}"
    )

    return response.json()

@pytest.fixture
def customer(client, auth_headers):
    response = client.post(
        "/customer/",
        json={
            "first_name": "John",
            "last_name": "Customer",
            "phone_no": "0700000000",
            "address": "Nairobi",
            "is_active": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Customer creation failed: {response.text}"
    )

    return response.json()
@pytest.fixture
def sale(client, auth_headers, customer):
    response = client.get(
        "/user/",
        headers=auth_headers,
    )

    assert response.status_code == 200, (
        f"User lookup failed: {response.text}"
    )

    users = response.json()

    user = next(
        user
        for user in users
        if user["username"] == "testuser"
    )

    response = client.post(
        "/sale/",
        json={
            "customer_id": customer["customer_id"],
            "user_id": user["user_id"],
            "sale_date": "2026-09-20T10:00:00Z",
            "subtotal": "10.00",
            "tax_amount": "1.60",
            "discount_amount": "0.00",
            "total_amount": "11.60",
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Sale creation failed: {response.text}"
    )
    

    return response.json()

@pytest.fixture
def payment(client, auth_headers, sale):
    response = client.post(
        "/payment/",
        json={
            "sale_id": sale["sale_id"],
            "amount": "11.60",
            "payment_method": "cash",
            "status": "completed",
            "payment_date": "2026-09-20T10:00:00Z",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, (
        f"Payment creation failed: {response.text}"
    )

    return response.json()
@pytest.fixture
def supplier(client, auth_headers):
    response = client.post(
        "/supplier/",
        json={
            "company_name": "Test Supplier Ltd",
            "contact_name": "John Supplier",
            "email": "supplier@example.com",
            "phone_no": "0712345678",
            "address": "Nairobi",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201, f"Supplier creation failed: {response.text}"
    return response.json()

@pytest.fixture
def receipt(client, auth_headers, sale):
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

    assert response.status_code == 201, (
        f"Receipt creation failed: {response.text}"
    )

    return response.json()