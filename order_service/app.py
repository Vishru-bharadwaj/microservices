from flask import Flask, jsonify, request

app = Flask(__name__)

# Initial orders with payment fields
orders = [
    {"id": 1, "user_id": 1, "item": "Laptop", "transaction_status": None, "transaction_id": None},
    {"id": 2, "user_id": 2, "item": "Phone", "transaction_status": None, "transaction_id": None}
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    return jsonify(order) if order else ("Order not found", 404)

@app.route('/orders', methods=['POST'])
def add_order():
    new_order = request.json
    new_order["id"] = len(orders) + 1
    new_order["transaction_status"] = "pending"
    new_order["transaction_id"] = None
    orders.append(new_order)
    return jsonify(new_order), 201

# New endpoint to update payment details for an order.
@app.route('/orders/<int:order_id>/payment', methods=['PUT'])
def update_payment_status(order_id):
    data = request.json
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order not found", 404
    order["transaction_status"] = data.get("transaction_status")
    order["transaction_id"] = data.get("transaction_id")
    return jsonify(order)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
