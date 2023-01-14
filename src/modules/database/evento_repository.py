from modules.models.Evento import Evento
from modules.database.connection import db
from pony.flask import db_session
from pony.orm import select


@db_session
def add_event(nome, hr_inicio, hr_fim, descricao, notificar, curent_user):
    Evento(
        nome=nome,
        dt_hr_inicio=hr_inicio,
        dt_hr_fim=hr_fim,
        descricao=descricao,
        notificar=notificar,
        usuario=curent_user,
        status=1,
    )


def get_all_user_events(current_user):
    print(db.Usuario.get(id=current_user.id).eventos)
    return select(event for event in Evento if event.usuario == current_user)[:]
