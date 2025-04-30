# Creates the web application instance
# Read the JSON body in a POST request
# Converts Python dictionaries into properly formatted JSON responses
from flask import Flask, request, jsonify

# Load and save sessions in storage.json
import json 

# Random short codes
import random

# Randomly pick characters for short codes
import string

# Get current time, parse timestamps, time differences
from datetime import datetime, timedelta

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

# Remove sessions older than 24 hours
def remove_expired_sessions(sessions):
    now = datetime.utcnow()
    expired_codes = []

    for code, session in sessions.items():
        timestamp = datetime.fromisoformat(session["timestamp"])
        if now - timestamp > timedelta(hours=24):
            expired_codes.append(code)

    for code in expired_codes:
        del sessions[code]

    if expired_codes:
        save_sessions(sessions)

# Generate a short random 6-character code
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# POST /session: create a session
@app.route("/session", methods=["POST"])
def create_session():
    data = request.get_json()
    license_plate = data.get("license_plate")
    lot_id = data.get("lot_id")
    custom_code = data.get("custom_code")

    if not license_plate or not lot_id:
        return jsonify({"error": "license_plate and lot_id are required"}), 400

    sessions = load_sessions()
    remove_expired_sessions(sessions)

    # Use custom code if provided
    if custom_code:
        if custom_code in sessions:
            return jsonify({"error": "Custom code already in use"}), 400
        code = custom_code
    else:
        code = generate_code()
        while code in sessions:
            code = generate_code()

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
    remove_expired_sessions(sessions)
    session = sessions.get(code)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(session)

# Homepage route
@app.route("/")
def index():
    return "🚗 Parking Shortener API is running!"

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")