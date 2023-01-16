from src.modules.models.Evento import Evento
from src.modules.database.connection import db
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


def get_event_by_id(event_id):
    return db.Evento.get(id=event_id)


def get_all_user_events(current_user):
    events = select(
        event for event in Evento if event.usuario == current_user and event.status == 1
    )[:]
    return convert_events_to_json(events)


@db_session
def update_event(id, nome, data, hora, descricao, notificar):
    event = get_event_by_id(id)
    event.nome = nome
    event.data = data
    event.hora = hora
    event.descricao = descricao
    event.notificar = notificar


@db_session
def delete_event(id):
    event = get_event_by_id(id)
    event.status = 0
