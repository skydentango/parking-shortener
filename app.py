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

# Creates the Flask application object
app = Flask(__name__)

# Defines the name of file where data will be stored
STORAGE_FILE = "storage.json"

# Opens storage.json, read the JSON inside, returns it as Python dictionary
# If fails, returns blank dictionary
def load_sessions():
    try:
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    except:
        return {}

# Opens storage.json, converts python dictionary to JSON, writes data into file
def save_sessions(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=2)

# Finds and deletes any sessions that are more than 24 hours old and saves the updated session list
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

# Handles POST session
# Validates the input, generates code, saves session in storage file, returns short code as response 
# Allows for a custom code if provided
# Error handling included
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

# Handles GET session
# Retrieves a saved parking session
# Looks up parking session by short code, deletes expired sessions, returns session if still exists
@app.route("/session/<code>", methods=["GET"])
def get_session(code):
    sessions = load_sessions()
    remove_expired_sessions(sessions)
    session = sessions.get(code)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify(session)

# Homepage
@app.route("/")
def index():
    return "Parking Shortener API is running!"

# Starts Flask server only when this file is run directly
# Ensures it is visible to browser inside GitHub Codespaces
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")