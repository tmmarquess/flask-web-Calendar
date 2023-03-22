from src.modules.models.Usuario import Usuario
from src.modules.database.connection import db
from pony.flask import db_session
from bcrypt import hashpw, gensalt, checkpw
from flask import make_response


@db_session
def add_user(name, email, password, birthday):
    Usuario(nome=name, email=email, senha=password, dt_nascimento=birthday, status=1)


@db_session
def add_user_api(user):
    if not get_user_by_email(user["user_email"]):
        Usuario(
            nome=user["user_name"],
            email=user["user_email"],
            senha=hashpw(user["user_password"].encode("utf-8"), gensalt()),
            dt_nascimento=user["user_birthday"],
            status=1,
        )
        return make_response(get_user_by_email(user["user_email"]).to_json(), 201)

    else:
        return make_response(
            f'User with email {user["user_email"]} already exists', 501
        )


def get_user_by_id_api(user_id):
    user = get_user_by_id(user_id)
    if user:
        return make_response(user.to_json(), 200)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def get_user_by_id(user_id):
    return db.Usuario.get(id=user_id, status=1)


def get_user_by_email(user_email):
    return db.Usuario.get(email=user_email, status=1)


def read_all():
    users = list()
    for user in Usuario.select(lambda U: not U.status == 0):
        users.append(user.to_json())
    return users


@db_session
def update_user(id, name, email, birthday):
    user = get_user_by_id(id)

    user.nome = name
    user.email = email
    user.dt_nascimento = birthday


@db_session
def update_user_api(user_id, user):
    loaded_user = get_user_by_id(user_id)
    if loaded_user:
        update_user(
            user_id,
            user.get("user_name", loaded_user.nome),
            user.get("user_email", loaded_user.email),
            user.get("user_birthday", loaded_user.dt_nascimento),
        )
        return make_response(get_user_by_id_api(user_id))
    else:
        return make_response(f"User with id {user_id} not found", 404)


def change_password_api(user_id, passwords):
    if change_password(user_id, passwords["old_password"], passwords["new_password"]):
        return make_response("Password changed sucessfully", 201)
    else:
        return make_response("Something went wrong", 501)


@db_session
def change_password(id, oldPass, newPass):
    user = get_user_by_id(id)
    password_checked = checkpw(oldPass.encode("utf-8"), user.senha)

    if password_checked:
        user.senha = hashpw(newPass.encode("utf-8"), gensalt())
        return True
    else:
        return False


@db_session
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        user.status = 0
        return make_response(f"Sucessfully deleted user with id {user_id}", 204)
    else:
        return make_response(f"User with id {user_id} not found", 404)
