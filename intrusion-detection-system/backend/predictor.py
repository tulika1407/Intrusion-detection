from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import traceback
import os

# Create Flask app
app = Flask(__name__)
CORS(app)

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "models", "decision_tree.pkl")
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print(f"Model loaded from: {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Encoding maps (used in training)
protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
service_map = {"http": 0, "smtp": 1, "ftp": 2, "private": 3}  # Update according to your training
flag_map = {"SF": 0, "S0": 1, "REJ": 2}  # Add more if needed

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded."}), 500

        data = request.get_json()
        print("Data received:", data)

        # Convert categorical to numeric
        protocol_type = protocol_map.get(data["protocol_type"].lower(), -1)
        service = service_map.get(data["service"].lower(), -1)
        flag = flag_map.get(data["flag"].upper(), -1)

        if -1 in [protocol_type, service, flag]:
            return jsonify({"prediction": "Error: Unknown categorical value"})

        # Collect numerical features
        src_bytes = float(data["src_bytes"])
        dst_bytes = float(data["dst_bytes"])
        count = float(data["count"])
        same_srv_rate = float(data["same_srv_rate"])
        diff_srv_rate = float(data["diff_srv_rate"])
        dst_host_srv_count = float(data["dst_host_srv_count"])
        dst_host_same_src_port_rate = float(data["dst_host_same_src_port_rate"])

        # Only 10 features as per training
        features = np.array([[protocol_type, service, flag, src_bytes,
                              dst_bytes, count, same_srv_rate, diff_srv_rate,
                              dst_host_srv_count, dst_host_same_src_port_rate]])

        print("Features for prediction:", features)

        prediction = model.predict(features)[0]
        result = "Anomalous (Attack)" if prediction == 1 else "Safe (Normal)"
        return jsonify({"prediction": result})

    except Exception as e:
        print("Prediction error:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
