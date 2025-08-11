from flask import Flask, request, jsonify
from flask_cors import CORS
from inventory_ml import optimize_inventory

app = Flask(__name__)
CORS(app)  # Allow frontend requests

@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No JSON received"}), 400

        max_space = payload.get("max_space")
        data = payload.get("data")

        if not isinstance(max_space, (int, float)) or max_space <= 0:
            return jsonify({"error": "Invalid max_space"}), 400
        if not isinstance(data, list):
            return jsonify({"error": "data must be a list"}), 400

        result = optimize_inventory(max_space, data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
