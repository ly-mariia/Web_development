import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_auth(token: str = Depends(oauth2_scheme)):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tokens WHERE token=?", (token,))
    user = c.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping", tags=["ping"])
async def ping_pong(
    token: str = Depends(check_auth)
):
    return token

@app.get("/items/", tags=["items"])
async def read_items(_: str = Depends(check_auth)):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    return [{"id": item[0], "name": item[1], "price": item[2]} for item in items]


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int, _: str = Depends(check_auth)):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = c.fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", tags=["items"])
async def create_item(name: str, price: float):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()
    return {"name": name, "price": price}

@app.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: int, name: str, price: float):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("UPDATE items SET name=?, price=? WHERE id=?", (name, price, item_id))
    conn.commit()
    conn.close()
    return {"name": name, "price": price}

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}


@app.get("/cart/", tags=["cart"])
async def read_cart():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart")
    cart = c.fetchall()
    conn.close()
    return cart

@app.get("/cart/{cart_id}", tags=["cart"])
async def read_cart_item(cart_id: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart WHERE id=?", (cart_id,))
    cart_item = c.fetchone()
    conn.close()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item

@app.post("/cart/", tags=["cart"])
async def create_cart(item_id: int, quantity: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("INSERT INTO cart (item_id, quantity) VALUES (?, ?)", (item_id, quantity))
    conn.commit()
    conn.close()
    return {"item_id": item_id, "quantity": quantity}

@app.put("/cart/{cart_id}", tags=["cart"])
async def update_cart(cart_id: int, item_id: int, quantity: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("UPDATE cart SET item_id=?, quantity=? WHERE id=?", (item_id, quantity, cart_id))
    conn.commit()
    conn.close()
    return {"item_id": item_id, "quantity": quantity}

@app.delete("/cart/{cart_id}", tags=["cart"])
async def delete_cart(cart_id: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE id=?", (cart_id,))
    conn.commit()
    conn.close()
    return {"message": "Cart item deleted successfully"}

@app.get("/orders/", tags=["orders"])
async def read_orders():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    conn.close()
    return orders

@app.get("/orders/{order_id}", tags=["orders"])
async def read_order(order_id: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = c.fetchone()
    conn.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders/", tags=["orders"])
async def create_order(item_id: int, quantity: int, status: str):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (?, ?, ?)", (item_id, quantity, status))
    conn.commit()
    conn.close()
    return {"item_id": item_id, "quantity": quantity, "status": status}

@app.put("/orders/{order_id}", tags=["orders"])
async def update_order(order_id: int, item_id: int, quantity: int, status: str):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("UPDATE orders SET item_id=?, quantity=?, status=? WHERE id=?", (item_id, quantity, status, order_id))
    conn.commit()
    conn.close()
    return {"item_id": item_id, "quantity": quantity, "status": status}

@app.delete("/orders/{order_id}", tags=["orders"])
async def delete_order(order_id: int):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully"}


@app.get("/cart_items/", tags=["nested"])
async def read_cart_items():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart")
    cart = c.fetchall()
    cart_items = []
    for item in cart:
        c.execute("SELECT * FROM items WHERE id=?", (item[1],))
        item_info = c.fetchone()
        cart_items.append({"item": {"name": item_info[1], "price": item_info[2]}, "quantity": item[2], "total": item_info[2] * item[2]})
    conn.close()
    return cart_items


@app.get("/cart_items_sorted/", tags=["sorting"])
async def read_cart_items_sorted(page: int = 1, limit: int = 10, sort_by: str = "name", order: str = "asc",_: str = Depends(check_auth)):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart")
    cart = c.fetchall()
    cart_items = []
    for item in cart:
        c.execute("SELECT * FROM items WHERE id=?", (item[1],))
        item_info = c.fetchone()
        cart_items.append({"item": {"name": item_info[1], "price": item_info[2]}, "quantity": item[2], "total": item_info[2] * item[2]})
    conn.close()
    if sort_by == "name":
        cart_items = sorted(cart_items, key=lambda x: x["item"]["name"], reverse=(order == "desc"))
    elif sort_by == "price":
        cart_items = sorted(cart_items, key=lambda x: x["item"]["price"], reverse=(order == "desc"))
    elif sort_by == "quantity":
        cart_items = sorted(cart_items, key=lambda x: x["quantity"], reverse=(order == "desc"))
    elif sort_by == "total":
        cart_items = sorted(cart_items, key=lambda x: x["total"], reverse=(order == "desc"))
    start = (page - 1) * limit
    end = start + limit
    return cart_items[start:end]
