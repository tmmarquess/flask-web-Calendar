import modules.database.evento_repository as evento_repository
from resources.app import app
from flask import redirect, request, render_template
from flask_login import current_user, login_required


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
        print(bool(request.form.get("notificar")))
        print("==========================")
        evento_repository.add_event(
            request.form["nome"],
            request.form["hr_inicio"],
            request.form["hr_fim"],
            request.form["descricao"],
            bool(request.form.get("notificar")),
            current_user,
        )
        return redirect("/")
