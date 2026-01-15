from flask import Flask, render_template, request, jsonify, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

DATA_FILE = "records.json"


def load_records():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    records = load_records()
    records.append(data)
    save_records(records)
    return jsonify({"status": "ok"})


@app.route("/list")
def list_records():
    return jsonify(load_records())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin.html", records=load_records())


@app.route("/delete", methods=["POST"])
def delete():
    if not session.get("admin"):
        return jsonify({"error": "unauthorized"}), 403

    index = request.get_json().get("index")
    records = load_records()

    if 0 <= index < len(records):
        records.pop(index)
        save_records(records)
        return jsonify({"status": "deleted"})

    return jsonify({"error": "invalid index"}), 400


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
