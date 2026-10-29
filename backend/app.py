from flask import Flask, jsonify

app = Flask(__name__)

data = [
    {"id": 1, "name": "Dev", "course": "Python"},
    {"id": 2, "name": "Rahul", "course": "Flask"},
    {"id": 3, "name": "Priya", "course": "Web Development"}
]


@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running"})


@app.route("/api")
def api():
    return jsonify(data)


@app.route("/submit", methods=["POST"])
def submit():
    return jsonify({
        "message": "Submission received successfully"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
