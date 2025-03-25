from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    # Simulate payment processing by generating a unique transaction ID.
    transaction_id = str(uuid.uuid4())
    return jsonify({
        "status": "success",
        "transaction_id": transaction_id,
        "order_id": data.get("order_id"),
        "amount": data.get("amount")
    }), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)
