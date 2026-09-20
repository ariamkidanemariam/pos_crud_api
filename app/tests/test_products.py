from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_lsit_product():
    response= client.get("/product")
    assert response.status_code == 200
   
def test_create_product():
    product_data ={
        "name": "Coca cola",
        "price": 103,
        "category_id": 165
    } 
    
    response= client.post("/products", json =product_data)
    assert response.status_code == 201