from modules.models.Usuario import Usuario
from modules.database.connection import db
from pony.flask import db_session


@db_session
def add_user(name, email, password, birthday):
    Usuario(nome=name, email=email, senha=password, dt_nascimento=birthday, status=1)


def get_user_by_id(user_id):
    return db.Usuario.get(id=user_id)


def get_user_by_email(user_email):
    return db.Usuario.get(email=user_email)
