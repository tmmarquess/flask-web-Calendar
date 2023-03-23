from src.modules.models.Usuario import Usuario
from src.modules.database.connection import db
from pony.flask import db_session
from bcrypt import hashpw, gensalt, checkpw


@db_session
def add_user(name, email, password, birthday):
    return Usuario(
        nome=name, email=email, senha=password, dt_nascimento=birthday, status=1
    )


def get_user_by_id(user_id):
    return db.Usuario.get(id=user_id, status=1)


def get_user_by_email(user_email):
    return db.Usuario.get(email=user_email, status=1)


@db_session
def update_user(id, name, email, birthday):
    user = get_user_by_id(id)

    user.nome = name
    user.email = email
    user.dt_nascimento = birthday


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
        return True
    else:
        return False
