# Parking Session Shortener API

Python + Flask API that allows users to create and retrieve parking sessions using a short code
Runs in GitHub Codespacee and uses a local JSON file storage

---

## 📦 Features

- `POST /session` – Create a new parking session
- `GET /session/<short_code>` – Retrieve a session by its code
- Sessions stored in a local JSON file
- Automatic removal of sessions older than 24 hours
- Optional **custom short codes**
- Input validation and error handling
- Friendly homepage route (`/`) for quick server check

---


## 🚀 How to Run (in GitHub Codespaces)

1. **Open this repo in a Codespace**

2. In the terminal, set up the environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

3. Start the Flask app:

```bash
python app.py
```

4. You’ll see:
```
Running on http://0.0.0.0:5000
```

---

## 🧪 How to Test

### ➕ Create a Session (Random Short Code)

```bash
curl -X POST http://127.0.0.1:5000/session \
  -H "Content-Type: application/json" \
  -d '{"license_plate": "XYZ123", "lot_id": "Lot42"}'
```

📬 Example response:
```json
{ "short_code": "aB7x3Z" }
```

---

### ➕ Create a Session (Custom Short Code)

```bash
curl -X POST http://127.0.0.1:5000/session \
  -H "Content-Type: application/json" \
  -d '{"license_plate": "ZZZ999", "lot_id": "GarageA", "custom_code": "MYCAR99"}'
```

📬 Response:
```json
{ "short_code": "MYCAR99" }
```

---

### 🔍 Retrieve a Session

```bash
curl http://127.0.0.1:5000/session/MYCAR99
```

📬 Example response:
```json
{
  "license_plate": "ZZZ999",
  "lot_id": "GarageA",
  "timestamp": "2025-04-30T14:00:00"
}
```

---

### ❌ Try an Expired Session

If a session is older than 24 hours, it will be deleted and return:

```json
{ "error": "Session not found" }
```

---

## 💡 Error Handling

- Missing `license_plate` or `lot_id` → `400 Bad Request`
- Duplicate custom code → `400 Bad Request`
- Not found → `404 Not Found`
- Expired → Session is deleted automatically

