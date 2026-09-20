# Point of Sale (POS) Backend API

A backend REST API for managing the core operations of a Point of Sale (POS) system. The application provides endpoints for users, products, categories, suppliers, customers, sales, sale items, payments, and receipts.

The project is built with **Python, FastAPI, SQLAlchemy, and Pydantic** and includes automated tests and continuous integration through GitHub Actions.

## Features

- User registration and authentication
- Role-based access control
- Product management
- Category management
- Supplier management
- Customer management
- Sales management
- Sale item management
- Payment management
- Receipt management
- Request validation using Pydantic
- Database interaction using SQLAlchemy
- Automated test suite with pytest
- Continuous integration using GitHub Actions

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request and response validation |
| PostgreSQL | Application database |
| SQLite | Database used during automated tests |
| Pytest | Automated testing |
| GitHub Actions | Continuous integration |

---

## Project Structure

```text
pos/
│
├── app/
│   ├── core/
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── customer.py
│   │   ├── sale.py
│   │   ├── sale_item.py
│   │   ├── payment.py
│   │   └── receipt.py
│   │
│   ├── repositories/
│   │   └── ...
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── services/
│   │   └── ...
│   │
│   ├── routers/
│   │   └── ...
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth_service.py
│       ├── test_user.py
│       ├── test_product.py
│       ├── test_category.py
│       ├── test_supplier.py
│       ├── test_customer.py
│       ├── test_sale.py
│       ├── test_sale_item.py
│       ├── test_payment.py
│       └── test_receipt.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── database.py
├── main.py
├── requirements.txt
├── pytest.ini
└── README.md

## Running Tests

To run the complete test suite locally, install the project dependencies:

```bash
pip install -r requirements.txt
