from flask import Flask, request, render_template, jsonify
import mysql.connector
import random
import string

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'hrishi@2006',  # Replace with your MySQL password
    'database': 'courier_service'  # Replace with your database name
}

# Function to connect to MySQL database
def get_db():
    conn = mysql.connector.connect(**db_config)
    return conn

# Route to serve the order form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle placing an order
@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    
    # Generate a random tracking ID
    tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Insert the order into the MySQL database
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (name, address, phone, tracking_id) VALUES (%s, %s, %s, %s)',
                       (name, address, phone, tracking_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return f"Order placed successfully! Your tracking ID is: {tracking_id}"
    except Exception as e:
        print("Error:", e)
        return f"Error occurred while placing the order: {e}"

# Route to handle order tracking
@app.route('/track_order', methods=['POST'])
def track_order():
    tracking_id = request.form['trackingId']
    
    # Assuming you have a function to retrieve the order by tracking ID
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE tracking_id = %s', (tracking_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if order:
            return f"Order found: {order}"
        else:
            return "No order found with that tracking ID."
    except Exception as e:
        print("Error:", e)
        return f"Error occurred while tracking the order: {e}"

if __name__ == '__main__':
    app.run(debug=True)
