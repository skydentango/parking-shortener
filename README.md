# 🚗 Simple Parking Session Shortener (Flask API)

This project is a lightweight web service that allows users to create and retrieve short codes for parking sessions using a simple REST API.

Built with **Python + Flask**, designed to run inside **GitHub Codespaces**, and stores session data in a local JSON file.

---

## ⚙️ Features

- `POST /session`: Create a parking session with a license plate and lot ID
- `GET /session/<short_code>`: Retrieve a session by its short code
- Session data is saved in `storage.json`
- Validates input and handles errors
- No large frameworks used (Flask only)

---

## 🚀 How to Run (in GitHub Codespaces)

1. **Create your Codespace** from this repository

2. **Set up environment** (in the terminal):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run the Flask app**:

```bash
python app.py
```

You’ll see output like:

```
Running on http://0.0.0.0:5000
```

---

## 🧪 How to Test the API

### ✅ POST /session

```bash
curl -X POST http://127.0.0.1:5000/session \
  -H "Content-Type: application/json" \
  -d '{"license_plate": "ABC123", "lot_id": "Lot42"}'
```

📬 Response:

```json
{
  "short_code": "abc123"
}
```

---

### 🔍 GET /session/<short_code>

```bash
curl http://127.0.0.1:5000/session/abc123
```

📬 Response:

```json
{
  "license_plate": "ABC123",
  "lot_id": "Lot42",
  "timestamp": "2025-04-30T..."
}
```

---

## 🧠 Notes

- All data is stored in a local file: `storage.json`
- Make sure to activate your virtual environment before running
- This app is intended for educational/testing purposes — not production use

---

## 🏁 Done!

This project satisfies all requirements for the Parking Session Shortener task. ✅
