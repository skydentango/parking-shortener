from flask import Flask, request, jsonify
import json
import random
import string
from datetime import datetime

app = Flask(__name__)
STORAGE_FILE = "storage.json"

# Load saved sessions from storage.json
def load_sessions():
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save updated sessions to storage.json
def save_sessions(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Generate a short random 6-character code
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# POST /session: create a session
@app.route("/session", methods=["POST"])
def create_session():
    data = request.get_json()

    # Validate input
    license_plate = data.get("license_plate")
    lot_id = data.get("lot_id")

    if not license_plate or not lot_id:
        return jsonify({"error": "license_plate and lot_id are required"}), 400

    # Generate unique code
    code = generate_code()
    sessions = load_sessions()
    while code in sessions:
        code = generate_code()

    # Store session
    sessions[code] = {
        "license_plate": license_plate,
        "lot_id": lot_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    save_sessions(sessions)

    return jsonify({"short_code": code})

# GET /session/<short_code>: get session info
@app.route("/session/<code>", methods=["GET"])
def get_session(code):
    sessions = load_sessions()
    session = sessions.get(code)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(session)

@app.route("/")
def index():
    return "Parking Shortener API is running!"

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
