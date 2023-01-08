from flask import Flask, render_template, request, flash, redirect
from flask_login import login_manager, LoginManager, login_user
from pony.flask import Pony, db_session
import models

app = Flask(__name__)
app.secret_key = "mySuperSecretKey"

Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(email, password):
    possible_user = models.db.Usuario.get(email=email)
    if not possible_user:
        return redirect("/login")
    if possible_user.senha == password:
        login_user(possible_user)
        return str(possible_user.nome + possible_user.email)


# ------------------ Database ----------------


@db_session
def add_user(name, email, password, birthday):
    models.Usuario(
        nome=name, email=email, senha=password, dt_nascimento=birthday, status=1
    )


# ------------------ Routes ----------------


@app.route("/")
def index():
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
        return load_user(request.form["email"], request.form["password"])
