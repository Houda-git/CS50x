from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import datetime, date
import json

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
            return apology("Must provide username and password", 403)

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
            return apology("Invalid input", 400)

        # Hash password and insert into database
        try:
            pw_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pw_hash)
            return redirect("/")
        except Exception as e:
            print("Registration error:", e)
            return apology("Username already taken", 400)
    else:
        return render_template("register.html")

@app.route("/", methods=["GET"])
@login_required
def index():
    """Show categories with enhanced statistics"""
    categories = db.execute("""
        SELECT c.id, c.name, c.color, c.icon,
               COUNT(t.id) as total_tasks,
               COUNT(CASE WHEN t.completed = 1 THEN 1 END) as completed_tasks
        FROM categories c
        LEFT JOIN tasks t ON c.id = t.category_id
        WHERE c.user_id = ?
        GROUP BY c.id, c.name, c.color, c.icon
        ORDER BY c.created_at DESC
    """, session["user_id"])

    # Calculate completion percentages
    for category in categories:
        if category['total_tasks'] > 0:
            category['completion_percentage'] = round((category['completed_tasks'] / category['total_tasks']) * 100)
        else:
            category['completion_percentage'] = 0

    total_categories = len(categories)
    total_tasks = sum(cat['total_tasks'] for cat in categories)
    total_completed = sum(cat['completed_tasks'] for cat in categories)
    overall_completion = round((total_completed / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template("index.html",
                           categories=categories,
                           total_categories=total_categories,
                           total_tasks=total_tasks,
                           total_completed=total_completed,
                           overall_completion=overall_completion)

@app.route("/add_category", methods=["POST"])
@login_required
def add_category():
    """Add personalized categories with color and icon"""
    name = request.form.get("category_name")
    icon = request.form.get("category_icon")
    status= request.form.get("status","Not started")

    if not name:
        return jsonify({"error": "Category name cannot be empty"}), 400

    existing = db.execute("SELECT id FROM categories WHERE user_id = ? AND name = ?", session["user_id"], name)
    if existing:
        return jsonify({"error": "Category name already exists"}), 409

    try:
        new_id = db.execute("""
            INSERT INTO categories (user_id, name, icon, status)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], name, icon,status)

        return jsonify({
            "id": new_id,
            "name": name,
            "icon": icon,
            "total_tasks": 0,
            "completed_tasks": 0,
            "completion_percentage": 0
        }), 200
    except Exception as e:
        print("Error adding category:", e)
        return jsonify({"error": "Could not add category"}), 400

@app.route("/category/<int:category_id>", methods=["GET"])
@login_required
def category_tasks(category_id):
    """Show tasks for a category with enhanced features"""
    # Get tasks with due dates and priorities
    tasks = db.execute("""
        SELECT id, description, completed, priority, due_date, created_at
        FROM tasks
        WHERE user_id = ? AND category_id = ?
        ORDER BY
            CASE WHEN due_date IS NOT NULL THEN 0 ELSE 1 END,
            due_date ASC,
            priority DESC,
            created_at DESC
    """, session["user_id"], category_id)

    category = db.execute("SELECT name, color, icon FROM categories WHERE id = ? AND user_id = ?",
                         category_id, session["user_id"])

    if not category:
        return apology("Category not found", 404)

    # Process tasks for better display
    for task in tasks:
        if task['due_date']:
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            today = date.today()
            days_diff = (due_date - today).days

            if days_diff < 0:
                task['due_status'] = 'overdue'
                task['due_text'] = f"{abs(days_diff)} days overdue"
            elif days_diff == 0:
                task['due_status'] = 'today'
                task['due_text'] = 'Due today'
            elif days_diff == 1:
                task['due_status'] = 'tomorrow'
                task['due_text'] = 'Due tomorrow'
            else:
                task['due_status'] = 'upcoming'
                task['due_text'] = f"Due in {days_diff} days"
        else:
            task['due_status'] = 'none'
            task['due_text'] = ''

    return render_template("task.html",
                         tasks=tasks,
                         category=category[0],
                         category_id=category_id)

@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    """Add a task with enhanced features"""
    task_name = request.form.get("task_name")
    category_id = request.form.get("category_id")
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date")

    if not task_name:
        return jsonify({"error": "Task name cannot be empty"}), 400

    try:
        task_id = db.execute("""
            INSERT INTO tasks (user_id, category_id, description, priority, due_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, session["user_id"], category_id, task_name, priority, due_date, datetime.now())

        return jsonify({
            "id": task_id,
            "description": task_name,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }), 200
    except Exception as e:
        print("Error adding task:", e)
        return jsonify({"error": "Could not add task"}), 400

@app.route("/update_task_status", methods=["POST"])
@login_required
def update_task_status():
    """Update task completion status"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    task_id = data.get("task_id")
    is_completed = data.get("completed")

    if task_id is None or is_completed is None:
        return jsonify({"error": "Missing info"}), 400

    try:
        db.execute("UPDATE tasks SET completed = ? WHERE id = ? AND user_id = ?",
                  1 if is_completed else 0, task_id, session["user_id"])
        return jsonify({"success": True}), 200
    except Exception as e:
        print("Error updating task:", e)
        return jsonify({"success": False, "error": "Could not update task"}), 400

@app.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    """Delete a task"""
    data = request.get_json()
    task_id = data.get("task_id")

    if not task_id:
        return jsonify({"error": "Task ID required"}), 400

    try:
        db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
        return jsonify({"success": True}), 200
    except Exception as e:
        print("Error deleting task:", e)
        return jsonify({"success": False, "error": "Could not delete task"}), 400

@app.route("/delete_category", methods=["POST"])
@login_required
def delete_category():
    """Delete a category and all its tasks"""
    data = request.get_json()
    category_id = data.get("category_id")

    if not category_id:
        return jsonify({"error": "Category ID required"}), 400

    try:
        # Delete all tasks in the category first
        db.execute("DELETE FROM tasks WHERE category_id = ? AND user_id = ?", category_id, session["user_id"])
        # Then delete the category
        db.execute("DELETE FROM categories WHERE id = ? AND user_id = ?", category_id, session["user_id"])
        return jsonify({"success": True}), 200
    except Exception as e:
        print("Error deleting category:", e)
        return jsonify({"success": False, "error": "Could not delete category"}), 400

@app.route("/stats")
@login_required
def stats():
    """Show user statistics"""
    stats_data = db.execute("""
        SELECT
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN completed = 1 THEN 1 END) as completed_tasks,
            COUNT(CASE WHEN completed = 0 THEN 1 END) as pending_tasks
        FROM tasks
        WHERE user_id = ?
    """, session["user_id"])[0]

    category_stats = db.execute("""
        SELECT c.name, c.color, c.icon,
               COUNT(t.id) as total_tasks,
               COUNT(CASE WHEN t.completed = 1 THEN 1 END) as completed_tasks
        FROM categories c
        LEFT JOIN tasks t ON c.id = t.category_id
        WHERE c.user_id = ?
        GROUP BY c.id, c.name, c.color, c.icon
        HAVING COUNT(t.id) > 0
        ORDER BY total_tasks DESC
    """, session["user_id"])

    return render_template("stats.html", stats=stats_data, category_stats=category_stats)

if __name__ == '__main__':
    app.run(debug=True)
