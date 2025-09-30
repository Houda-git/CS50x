import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user's cash
    user = db.execute("SELECT cash FROM users WHERE id= ?", session["user_id"])
    cash = user[0]["cash"]

    # Get user's stocks
    rows = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    portfolio = []
    total_stock_value = 0

    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]
        stock = lookup(symbol)  # So that we can get the current price
        if stock:  # make sure the symbol is valid
            price = stock["price"]
            total = shares * price
            total_stock_value += total
            portfolio.append({
                "symbol": symbol,
                "name": stock["name"],
                "shares": shares,
                "price": price,  # current price per share
                "total": total  # total value
            })

    grand_total = cash + total_stock_value

    return render_template("index.html", cash=cash, portfolio=portfolio, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Must provide symbol", 400)
        result = lookup(symbol)
        if result is None:
            return apology("Symbol not found", 400)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid share", 400)
        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = user[0]["cash"]  # the cash that the user has
        price = int(shares) * result["price"]
        if cash < price:
            return apology("Not enough cash", 400)
        db.execute("UPDATE users SET cash = cash - ? where id = ?", price, session["user_id"])
        db.execute("INSERT INTO transactions(user_id, symbol, shares,price) VALUES(?,?,?,?)",
                   session["user_id"], symbol, shares, result["price"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT symbol,shares,price,transacted FROM transactions WHERE user_id = ?", session["user_id"])
    history = []
    for row in rows:
        state = "SELL" if row["shares"] < 0 else "BUY"
        history.append({
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": row["price"],
            "transacted": row["transacted"],
            "state": state
        })
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must provide symbol", 400)
        result = lookup(symbol)
        if result is None:
            return apology("Symbol not found", 400)
        return render_template("quoted.html", stock=result)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("Username required", 400)
        if not password:
            return apology("Password required", 400)
        if password != confirmation:
            return apology("The passwords don't match", 400)
        pw_hash = generate_password_hash(password)
        try:
            db.execute('INSERT INTO users(username,hash) VALUES (?,?)', username, pw_hash)
        except:
            return apology("Username already used", 400)
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_c = request.form.get("shares")
        if not symbol:
            return apology("Symbol not found", 400)
        stock = lookup(symbol)
        if stock is None:
            return apology("Stock not found", 400)
        if not shares_c.isdigit() or int(shares_c) <= 0:
            return apology("No shares", 400)
        shares_c = int(shares_c)
        # We have to update the data after selling
        rows = db.execute(
            "SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?",
            session["user_id"], symbol
        )
        if len(rows) != 1 or rows[0]["total"] is None or rows[0]["total"] < shares_c:
            return apology("Not enough shares", 400)
        price = stock["price"] * shares_c
        db.execute("UPDATE users SET cash = cash + ? WHERE id= ?", price, session["user_id"])
        db.execute("INSERT INTO transactions (user_id,symbol,shares,price) VALUES(?,?,?,?)",
                   session["user_id"], symbol, -shares_c, stock["price"])
        return redirect("/")
    else:  # if not post just get
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares)>0", session["user_id"])
        return render_template("sell.html", symbols=symbols)
