from flask import Flask, render_template, request, flash, redirect
from flask_login import (
    login_manager,
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from pony.flask import Pony, db_session
import models

app = Flask(__name__)
app.secret_key = "mySuperSecretKey"

Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"


# ------------------ Database ----------------


@db_session
def add_user(name, email, password, birthday):
    models.Usuario(
        nome=name, email=email, senha=password, dt_nascimento=birthday, status=1
    )


def get_user(user_id=None, email=None):
    if email:
        return models.db.Usuario.get(email=email)
    elif user_id:
        return models.db.Usuario.get(id=user_id)


@login_manager.user_loader
def load_user(user_id):
    return models.db.Usuario.get(id=user_id)


@db_session
def authenticate_user(email, password):
    possible_user = get_user(email=email)
    if not possible_user:
        return redirect("/login")
    if possible_user.senha == password:
        login_user(possible_user)
        possible_user.authenticated = True

        # return redirect("/calendar")
        return redirect("/calendar")
    else:
        return redirect("/login")


# ------------------ Routes ----------------


@app.route("/")
def index():
    # return redirect("/calendar")
    return redirect("/login")


@app.route("/register", methods=["post", "get"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        add_user(
            request.form["name"],
            request.form["email"],
            request.form["password"],
            request.form["birthday"],
        )
        return redirect("/")


@app.route("/login", methods=["post", "get"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        return authenticate_user(request.form["email"], request.form["password"])


@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


@app.route("/logout")
@login_required
@db_session
def logout():
    current_user.authenticated = False
    logout_user()
    return redirect("/")