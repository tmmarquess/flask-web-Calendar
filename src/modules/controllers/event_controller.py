import modules.database.evento_repository as evento_repository
from resources.app import app
from flask import redirect, request, render_template
from flask_login import current_user, login_required


@app.route("/create_event", methods=["post", "get"])
@login_required
def create_event():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        evento_repository.add_event(
            request.form["nome"],
            request.form["data"],
            request.form["Hora"],
            request.form["descricao"],
            bool(int(request.form.get("notificar"))),
            current_user,
        )
        return redirect("/")


@app.route("/edit_event", methods=["post"])
def edit_event():
    evento_repository.update_event(
        request.form["id"],
        request.form["nome"],
        request.form["data"],
        request.form["Hora"],
        request.form["descricao"],
        bool(int(request.form.get("notificar"))),
    )
    return redirect("/")
