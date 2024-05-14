from flask import Flask, render_template, request, redirect, url_for
from dbb import *

app = Flask(__name__)

database = "user_database.db"
# conn = create_connection(database)

# Route for the login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         credentials = get_user_credentials(conn, username)
#         if credentials and credentials[1] == password:
#             return redirect(url_for('index'))
#         else:
#             # If credentials are incorrect, render login page with an error message
#             error = "Invalid username or password"
#             return render_template('login.html', error=error)
#     else:
#         # If the request method is GET, render the login page without any error message
#         return render_template('login.html', error="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = DatabaseManager.create_connection(database)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        credentials = DatabaseManager.get_user_credentials(conn, username)
        if credentials and credentials[0] == username and credentials[1] == password:
            # Login successful, redirect to index
            DatabaseManager.close_connection(conn)
            return redirect(url_for('index'))
        else:
            # Invalid credentials, display error message
            DatabaseManager.close_connection(conn)
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    else:
        # Render the login page
        DatabaseManager.close_connection(conn)
        return render_template('login.html', error="")



# @app.route('/insert_item', methods=['POST'])
# def insert_item():
#     # Extract item details from the request
#     name = request.form['name']
#     mail = request.form['Mail']
#     phone = request.form['phone']
#     item = request.form['item']
#     Quantity = request.form['Quantity']
#     price = request.form['price']
#     Delivery_address =request.form['Delivery_address']
#
#     # Connect to the SQLite database
#     conn = sqlite3.connect('user_database.db')
#     cursor = conn.cursor()
#
#     # Insert the item details into the database
#     cursor.execute('INSERT INTO items (name, price) VALUES (?, ?)', (name, price))
#
#     # Commit the transaction and close the connection
#     conn.commit()
#     conn.close()
#
#     return 'Item inserted successfully'


# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Route for processing registration data
@app.route('/registration', methods=['POST'])
def process_registration():
    conn = DatabaseManager.create_connection(database)

    username = request.form.get('username')
    password = request.form.get('password')
    DatabaseManager.create__user_table(conn)
    DatabaseManager.register_user(conn, username,password)
    return redirect(url_for('login'))

# Route for the veg page
@app.route('/veg')
def veg():
    return render_template('veg.html')

# Route for the nonveg page
@app.route('/nonveg')
def nonveg():
    return render_template('nonveg.html')

# Route for the fastfood page
@app.route('/fastfood')
def fastfood():
    return render_template('fastfood.html')

# Route for the contact page
@app.route('/contact')
def contact_form():
    return render_template('contact.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Here you can add code to process the form data, such as saving it to a database or sending it via email.

        return "Form submitted successfully! Thank you for contacting us, {}!".format(name)
@app.route('/submit_order', methods=['POST'])
def submit_order():
    conn = DatabaseManager.create_connection(database)
    DatabaseManager.create_order_table(conn)
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['Mail']
        phone = request.form['phone']
        item = request.form['item']
        quantity = request.form['Quantity']
        delivery_address = request.form['Delivery_address']

        DatabaseManager.insert_order(conn, name, mail, phone, item, quantity, delivery_address)
        DatabaseManager.close_connection(conn)
        return redirect(url_for('index'))

@app.route('/total_orders')
def total_orders():
    conn = DatabaseManager.create_connection(database)
    orders = DatabaseManager.get_orders(conn)
    DatabaseManager.close_connection(conn)

    # Parse and format order details for table rendering
    order_details = []
    for order in orders:
        order_id, customer_name, email, phone, product, quantity, delivery_info = order
        # delivery_info = delivery_info.split(',')  # Split delivery_info string
        order_details.append([order_id, product, quantity, delivery_info])

    return render_template('totalorders.html', order_details=order_details)



@app.route('/order')
def orders():
    conn = DatabaseManager.create_connection(database)
    orders = DatabaseManager.get_orders(conn)
    DatabaseManager.close_connection(conn)
    return render_template('order.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
