import sqlite3

class DatabaseManager:
    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    @staticmethod
    def close_connection(conn):
        if conn:
            conn.close()
            print("Connection closed.")

    @staticmethod
    def create__user_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL)''')
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def create_order_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT NOT NULL,
                                 mail TEXT NOT NULL,
                                 phone TEXT NOT NULL,
                                 item TEXT NOT NULL,
                                 quantity INTEGER NOT NULL,
                                 delivery_address TEXT NOT NULL)''')
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def insert_order(conn, name, mail, phone, item, quantity, delivery_address):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (name, mail, phone, item, quantity, delivery_address) VALUES (?, ?, ?, ?, ?, ?)",
                (name, mail, phone, item, quantity, delivery_address))
            conn.commit()
            print("Order inserted successfully!")
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def get_orders(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
    @staticmethod
    def register_user(conn, username, password):
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("User registered successfully!")
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def get_user_credentials(conn, username):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username=?", (username,))
            row = cursor.fetchone()
            if row:
                return row
            else:
                return None
        except sqlite3.Error as e:
            print(e)

# Example usage
# if __name__ == '__main__':
#     database = "user_database.db"
#     conn = DatabaseManager.create_connection(database)
#     if conn is not None:
#         DatabaseManager.create_table(conn)
#         DatabaseManager.register_user(conn, "ranji", "123456")
#         credentials = DatabaseManager.get_user_credentials(conn, "ranji")
#         if credentials:
#             print("Username:", credentials[0])
#             print("Password:", credentials[1])
#         else:
#             print("User not found.")
#         DatabaseManager.close_connection(conn)
#     else:
#         print("Error! cannot create the database connection.")
