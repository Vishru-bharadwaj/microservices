import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

USER_SERVICE_URL = "http://127.0.0.1:5001"
ORDER_SERVICE_URL = "http://127.0.0.1:5002"
PAYMENT_SERVICE_URL = "http://127.0.0.1:5003"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/users')
def users():
    response = requests.get(f"{USER_SERVICE_URL}/users")
    users_data = response.json()
    return render_template("users.html", users=users_data)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = {"name": name}
        requests.post(f"{USER_SERVICE_URL}/users", json=new_user)
        return redirect(url_for('users'))
    return render_template("add_user.html")

@app.route('/orders')
def orders():
    response = requests.get(f"{ORDER_SERVICE_URL}/orders")
    orders_data = response.json()
    return render_template("orders.html", orders=orders_data)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        user_id = request.form['user_id']
        item = request.form['item']
        new_order = {"user_id": int(user_id), "item": item}
        requests.post(f"{ORDER_SERVICE_URL}/orders", json=new_order)
        return redirect(url_for('orders'))
    return render_template("add_order.html")

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        order_id = request.form['order_id']
        amount = request.form['amount']
        new_payment = {"order_id": order_id, "amount": amount}
        payment_response = requests.post(f"{PAYMENT_SERVICE_URL}/pay", json=new_payment)
        payment_data = payment_response.json()
        # Update the order with the payment result:
        update_data = {
            "transaction_status": "completed",
            "transaction_id": payment_data["transaction_id"]
        }
        requests.put(f"{ORDER_SERVICE_URL}/orders/{order_id}/payment", json=update_data)
        return render_template("payment.html", payment=payment_data)
    return render_template("payment.html", payment=None)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
