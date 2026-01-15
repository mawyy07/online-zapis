from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"  # для сессий

DATA_FILE = "records.json"

# ====== НАСТРОЙКИ АДМИНА ======
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "1234"


def load_records():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_records(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html", is_admin=session.get("admin", False))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("index"))

        return render_template("login.html", error="Неверный логин или пароль")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    records = load_records()
    records.append(data)
    save_records(records)
    return jsonify({"status": "ok"})


@app.route("/list")
def get_list():
    return jsonify(load_records())


@app.route("/delete", methods=["POST"])
def delete():
    if not session.get("admin"):
        return jsonify({"status": "forbidden"}), 403

    data = request.get_json()
    index = data.get("index")

    records = load_records()
    if index is not None and 0 <= index < len(records):
        records.pop(index)
        save_records(records)

    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
