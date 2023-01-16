from src.modules.models.Usuario import Usuario
from src.modules.database.connection import db
from pony.flask import db_session
from src.resources.app import bcrypt


@db_session
def add_user(name, email, password, birthday):
    Usuario(nome=name, email=email, senha=password, dt_nascimento=birthday, status=1)


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
    password_checked = bcrypt.check_password_hash(user.senha, oldPass)

    if password_checked:
        user.senha = bcrypt.generate_password_hash(newPass)
        return True
    else:
        return False


@db_session
def delete_user(id):
    user = get_user_by_id(id)
    user.status = 0
