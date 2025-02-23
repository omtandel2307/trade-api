from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# Database Setup
conn = sqlite3.connect("orders.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        price REAL,
        quantity INTEGER,
        order_type TEXT
    )"""
)
conn.commit()

# Pydantic Model for Orders
class Order(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=5, pattern="^[A-Z]+$")
    price: float = Field(..., gt=0)  # Price must be greater than 0
    quantity: int = Field(..., gt=0) # Quantity must be greater than 0
    order_type: str = Field(..., pattern="^(buy|sell)$")  # Only "buy" or "sell"


# WebSocket connections
active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except:
        active_connections.remove(websocket)

async def notify_clients(order):
    for connection in active_connections:
        await connection.send_json(order)

# API Endpoints
@app.post("/orders")
async def create_order(order: Order):
    cursor.execute(
        "INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
        (order.symbol, order.price, order.quantity, order.order_type),
    )
    conn.commit()
    new_order = {"symbol": order.symbol, "price": order.price, "quantity": order.quantity, "order_type": order.order_type}
    await notify_clients(new_order)  # Send real-time updates
    return {"message": "Order created", "order": new_order}

@app.get("/orders")
def get_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return {"orders": [{"id": o[0], "symbol": o[1], "price": o[2], "quantity": o[3], "order_type": o[4]} for o in orders]}
