import sqlite3

conn = sqlite3.connect('items.db')

c = conn.cursor()

c.execute('''CREATE TABLE items
             (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')

c.execute("INSERT INTO items (name, price) VALUES ('apple', 0.99)")
c.execute("INSERT INTO items (name, price) VALUES ('banana', 0.59)")
c.execute("INSERT INTO items (name, price) VALUES ('cherry', 2.99)")

c.execute('''CREATE TABLE cart
                (id INTEGER PRIMARY KEY, item_id INTEGER, quantity INTEGER)''')

c.execute("INSERT INTO cart (item_id, quantity) VALUES (1, 2)")
c.execute("INSERT INTO cart (item_id, quantity) VALUES (2, 3)")
c.execute("INSERT INTO cart (item_id, quantity) VALUES (3, 1)")


c.execute('''CREATE TABLE orders
                (id INTEGER PRIMARY KEY, item_id INTEGER, quantity INTEGER, status TEXT)''')

c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (1, 2, 'pending')")
c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (2, 3, 'pending')")
c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (3, 1, 'pending')")
c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (1, 2, 'delivered')")
c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (2, 3, 'delivered')")
c.execute("INSERT INTO orders (item_id, quantity, status) VALUES (3, 1, 'delivered')")

c.execute('''CREATE TABLE tokens
                (id INTEGER PRIMARY KEY, token TEXT)''')

c.execute("INSERT INTO tokens (token) VALUES ('1234567890')")
c.execute("INSERT INTO tokens (token) VALUES ('0987654321')")
c.execute("INSERT INTO tokens (token) VALUES ('qwertyuiop')")

conn.commit()

conn.close()
