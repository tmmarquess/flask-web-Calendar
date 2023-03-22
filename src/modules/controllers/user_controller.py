from src.modules.database import usuario_repository
from src.resources.app import app
from flask import redirect, request, render_template
from flask_login import current_user, login_required, logout_user


@app.route("/user")
@login_required
def user_data():
    return render_template("user.html")


@app.route("/edit_user", methods=["get", "post"])
@login_required
def edit_user():
    if request.method == "GET":
        return render_template("edit_user.html")
    if request.method == "POST":
        usuario_repository.update_user(
            request.form["id"],
            request.form["name"],
            request.form["email"],
            request.form["birthday"],
        )
        return redirect("/calendar")


@app.route("/change_password", methods=["get", "post"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    if request.method == "POST":
        password_changed = usuario_repository.change_password(
            request.form["id"],
            request.form["oldPass"],
            request.form["newPass"],
        )
        if password_changed:
            return redirect("/")
        else:
            return redirect("/change_password")


@app.route("/delete_user", methods=["post"])
@login_required
def delete_user():
    usuario_repository.delete_user(current_user.id)
    logout_user()
    return redirect("/")
