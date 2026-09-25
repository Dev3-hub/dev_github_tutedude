from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from data import data

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["student_database"]
collection = db["students"]


@app.route("/api")
def api():
    return jsonify(data)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        course = request.form["course"]

        collection.insert_one({
            "name": name,
            "course": course
        })

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("form.html", error=str(e))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)