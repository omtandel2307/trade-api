from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

# Test case for invalid order type
def test_invalid_order_type():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "hold"  # Invalid order type (should be "buy" or "sell")
    })
    assert response.status_code == 422  # Expecting a validation error

# Test case for negative quantity
def test_negative_quantity():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": -10,  # Negative quantity
        "order_type": "buy"
    })
    assert response.status_code == 422  # Should reject negative quantity

# Test case for missing required fields
def test_missing_symbol():
    response = client.post("/orders", json={
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422  # Should reject due to missing "symbol"

def test_valid_order():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 200  # Successful order creation
    assert response.json()["message"] == "Order created"

def test_empty_payload():
    response = client.post("/orders", json={})
    assert response.status_code == 422  # Missing required fields

def test_missing_price():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422  # Missing "price" field

def test_negative_price():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": -150.0,  # Negative price
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422

def test_zero_quantity():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 0,  # Invalid quantity
        "order_type": "buy"
    })
    assert response.status_code == 422

def test_large_quantity():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 1000000000,  # Very large quantity
        "order_type": "buy"
    })
    assert response.status_code in [200, 422]  # Decide if you want to limit large orders

def test_case_insensitive_order_type():
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "BUY"  # Should be lowercase "buy" or "sell"
    })
    assert response.status_code == 422

def test_invalid_symbol():
    response = client.post("/orders", json={
        "symbol": "AAP$L!",  # Invalid characters
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422

def test_sql_injection():
    response = client.post("/orders", json={
        "symbol": "'; DROP TABLE orders; --",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422  # Should be rejected as invalid input

def test_long_symbol():
    response = client.post("/orders", json={
        "symbol": "TOOLONG",  # More than 5 chars
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    })
    assert response.status_code == 422