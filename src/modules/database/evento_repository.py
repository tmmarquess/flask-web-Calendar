from modules.models.Evento import Evento
from modules.database.connection import db
from pony.flask import db_session
from pony.orm import select
import json


@db_session
def add_event(nome, data, hora, descricao, notificar, curent_user):
    Evento(
        nome=nome,
        data=data,
        hora=hora,
        descricao=descricao,
        notificar=notificar,
        usuario=curent_user,
        status=1,
    )


def convert_events_to_json(events):
    events_list = []
    for event in events:
        events_list.append(
            dict(
                id=event.id,
                name=event.nome,
                day=event.data.day,
                month=event.data.month,
                year=event.data.year,
                time=event.hora,
                descricao=event.descricao,
                notificar=event.notificar,
                status=event.status,
                usuario=event.usuario.id,
            )
        )
    return events_list


def get_all_user_events(current_user):
    events = select(event for event in Evento if event.usuario == current_user)[:]
    return convert_events_to_json(events)
