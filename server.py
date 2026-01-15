from flask import Flask, render_template, request, jsonify
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Хранилище записей (в памяти)
records = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()

    records.append({
        "doctor": data.get("doctor"),
        "date": data.get("date"),
        "time": data.get("time")
    })

    return jsonify({"status": "ok"})

@app.route("/list")
def get_list():
    return jsonify(records)

@app.route("/delete", methods=["POST"])
def delete():
    data = request.get_json()
    index = data.get("index")

    if index is not None and 0 <= index < len(records):
        records.pop(index)
        return jsonify({"status": "deleted"})

    return jsonify({"status": "error"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

