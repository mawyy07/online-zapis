from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"  # ОБЯЗАТЕЛЬНО для авторизации

DATA_FILE = "records.json"

# ---------- утилиты ----------
def load_records():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ---------- страницы ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "admin123":  # пароль администратора
            session["admin"] = True
            return redirect(url_for("admin"))
        return "Неверный пароль", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

# ---------- API ----------
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
    if not session.get("admin"):
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json()
    index = data.get("index")

    records = load_records()
    if 0 <= index < len(records):
        records.pop(index)
        save_records(records)

    return jsonify({"status": "deleted"})

# ---------- запуск ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
