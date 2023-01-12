import modules.database as database
from resources.app import app, bcrypt, authenticate_user, db_session
from flask import redirect, request, render_template
from flask_login import current_user, login_required, logout_user


@app.route("/create_event", methods=["post", "get"])
@login_required
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")
    if request.method == "POST":
        print("==========================")
        print(request.form["nome"])
        print(request.form["hr_inicio"])
        print(type(request.form["hr_inicio"]))
        print(request.form["hr_fim"])
        print(request.form["descricao"])
        print((False if request.form.get("notificar") is None else True))
        print("==========================")
        database.add_event(
            request.form["nome"],
            request.form["hr_inicio"],
            request.form["hr_fim"],
            request.form["descricao"],
            (False if request.form.get("notificar") is None else True),
            current_user,
        )
        return redirect("/")
