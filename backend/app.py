# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import pandas as pd
from datetime import datetime
import joblib
import numpy as np
from utils.nonce_store import is_nonce_used, mark_nonce_used

app = Flask(__name__)
CORS(app)

# Paths
DATA_PATH = os.path.join("data", "behavior_log.json")
MODEL_PATH = os.path.join("models", "randomforest_bot_detector.joblib")
SCALER_PATH = os.path.join("models", "standard_scaler.joblib")

# Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Prediction features (same order as training)
FEATURE_NAMES = [
    "reaction_time",
    "answer_length",
    "avg_key_interval",
    "std_key_interval",
    "mouse_distance",
    "mouse_avg_speed",
    "mouse_movements"
]

@app.route("/api/submit", methods=["POST"])
def submit_data():
    try:
        data = request.get_json()

        # ✅ Check nonce
        nonce = data.get("nonce")
        if not nonce:
            return jsonify({"message": "Missing nonce"}), 400
        if is_nonce_used(nonce):
            return jsonify({"message": "Replay attack detected"}), 403
        mark_nonce_used(nonce)

        # ✅ Log IP (do not store)
        ip_addr = request.remote_addr
        print(f"[INFO] Submission from IP: {ip_addr}, Nonce: {nonce}")

        # ✅ Add timestamp
        data["timestamp"] = datetime.now().isoformat()

        # ✅ Save sanitized data (excluding IP, nonce)
        os.makedirs("data", exist_ok=True)
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r") as f:
                existing = json.load(f)
        else:
            existing = []

        existing.append(data)

        with open(DATA_PATH, "w") as f:
            json.dump(existing, f, indent=2)

        return jsonify({"message": "You're verified as human!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Something went wrong"}), 500

@app.route("/api/predict", methods=["POST"])
def predict_behavior():
    try:
        raw_data = request.get_json()

        # ✅ Extract features in training order
        input_features = [raw_data.get(feat, 0) for feat in FEATURE_NAMES]

        # ✅ Debugging print statements
        print("[DEBUG] Raw Data:", raw_data)
        print("[DEBUG] Extracted features:", input_features)

        # ✅ Convert to DataFrame to maintain column order
        input_df = pd.DataFrame([raw_data])[FEATURE_NAMES]
        scaled_input = scaler.transform(input_df)

        print("[DEBUG] Scaled input:", scaled_input)

        # ✅ Predict using model
        prediction = model.predict(scaled_input)[0]
        confidence = model.predict_proba(scaled_input)[0][int(prediction)]

        print("[DEBUG] Prediction:", prediction)
        print("[DEBUG] Confidence:", confidence)

        result = {
            "label": "bot" if prediction == 1 else "human",
            "confidence": round(float(confidence), 4)
        }

        return jsonify(result), 200

    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({"message": "Prediction failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
