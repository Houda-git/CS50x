import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    data = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    # Validate form data
    if not name or not month or not day:
        return redirect("/")

    birthday = {
        "name": name,
        "month": month,
        "day": day
    }

    db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

    return jsonify(birthday)
