import modules.database as database
from resources.app import app, bcrypt, authenticate_user, db_session
from flask import redirect, request, render_template
from flask_login import current_user, login_required, logout_user


@app.route("/")
def index():
    return redirect("/calendar")


@app.route("/register", methods=["post", "get"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        database.add_user(
            request.form["name"],
            request.form["email"],
            bcrypt.generate_password_hash(request.form["password"]),
            request.form["birthday"],
        )
        return redirect("/")


@app.route("/login", methods=["post", "get"])
def login():
    if current_user.is_authenticated:
        return redirect("/calendar")

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if authenticate_user(request.form["email"], request.form["password"]):
            return redirect("/calendar")
        else:
            return redirect("/login")


@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


@app.route("/logout")
@login_required
@db_session
def logout():
    current_user.set_authenticated(False)
    logout_user()
    return redirect("/")
