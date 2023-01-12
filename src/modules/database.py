from modules.models import db, Usuario, Evento
from pony.flask import db_session
from pony.orm import select


@db_session
def add_user(name, email, password, birthday):
    Usuario(nome=name, email=email, senha=password, dt_nascimento=birthday, status=1)


def get_user_by_id(user_id):
    return db.Usuario.get(id=user_id)


def get_user_by_email(user_email):
    return db.Usuario.get(email=user_email)


@db_session
def add_event(nome, hr_inicio, hr_fim, descricao, notificar, curent_user):
    Evento(
        nome=nome,
        dt_hr_inicio=hr_inicio,
        dt_hr_fim=hr_fim,
        descricao=descricao,
        notificar=notificar,
        usuario=curent_user,
        status=1
    )


def get_all_user_events(current_user):
    print(db.Usuario.get(id=current_user.id).eventos)
    return select(event for event in Evento if event.usuario == current_user)[:]
