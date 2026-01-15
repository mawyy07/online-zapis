from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "records.json"

# ---------- функции ----------
def load_records():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ---------- маршруты ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    records = load_records()
    data = request.get_json()
    records.append(data)
    save_records(records)
    return jsonify({"status": "ok"})

@app.route("/list")
def get_list():
    return jsonify(load_records())

@app.route("/delete", methods=["POST"])
def delete():
    records = load_records()
    index = request.get_json().get("index")

    if index is not None and 0 <= index < len(records):
        records.pop(index)
        save_records(records)
        return jsonify({"status": "deleted"})

    return jsonify({"status": "error"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
