from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database
db = SQL("sqlite:///todo.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        # Validate input
        if not request.form.get("username") or not request.form.get("password"):
            return apology("must provide username and password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember logged-in user
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username or not password or password != confirmation:
            return apology("invalid input", 400)

        # Hash password and insert into database
        try:
            pw_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pw_hash)
            return redirect("/")
        except Exception as e:
            print("Registration error:", e)
            return apology("username already taken", 400)
    else:
        return render_template("register.html")

@app.route("/", methods=["GET"])
@login_required
def index():
    """Show categories"""
    categories = db.execute("SELECT id, name FROM categories WHERE user_id = ?", session["user_id"])
    return render_template("index.html", categories=categories)

@app.route("/add_category", methods=["POST"])
@login_required
def add_category():
    """Add personalized categories"""
    name = request.form.get("category_name")
    if not name:
        return {"error": "Category name cannot be empty"}, 400
    existing = db.execute("SELECT id FROM categories where user_id = ? and name = ?", session["user_id"], name)
    if existing:
        return {"error": "Category name already existing"}, 409
    try:
        new_id = db.execute("INSERT INTO categories (user_id, name) VALUES (?, ?)", session["user_id"], name)
        return {"id": new_id, "name": name}, 200
    except Exception as e:
        print("Error adding category:", e)
        return {"error": "Could not add category"}, 400

@app.route("/category/<int:category_id>", methods=["GET"])
@login_required
def category_tasks(category_id):
    """Show tasks for a category"""
    tasks = db.execute("SELECT id, description, completed FROM tasks WHERE user_id = ? AND category_id = ?", session["user_id"], category_id)
    category = db.execute("SELECT name FROM categories WHERE id = ?", category_id)
    if not category:
        return apology("Category not found", 404)
    return render_template("task.html", tasks=tasks, category=category[0]["name"], category_id=category_id)

@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    """Add a task to a category"""
    task_name = request.form.get("task_name")
    category_id = request.form.get("category_id")

    if not task_name:
        return {"error": "Task name cannot be empty"}, 400

    try:
        db.execute("INSERT INTO tasks (user_id, category_id, description) VALUES (?, ?, ?)", session["user_id"], category_id, task_name)
        return {"description": task_name}, 200
    except Exception as e:
        print("Error adding task:", e)
        return {"error": "Could not add task"}, 400

@app.route("/update_task_status", methods=["POST"])
@login_required
def update_task_status():
    data = request.get_json()
    if not data:
        return {"success": False, "error": "Invalid JSON"}, 400
    task_id = data.get("task_id")
    is_completed = data.get("completed")
    if task_id is None or is_completed is None:
        return {"error: Missing info"}, 400
    db.execute("UPDATE tasks SET completed = ? WHERE id =? AND user_id = ?", 1 if is_completed else 0 , task_id, session["user_id"])
    return {"success": True}, 200


