import src.modules.database.evento_repository as evento_repository
import src.modules.database.usuario_repository as usuario_repository
from bcrypt import hashpw, gensalt, checkpw
from flask import make_response


def get_all_users():
    users = list()
    for user in usuario_repository.Usuario.select(lambda U: not U.status == 0):
        users.append(user.to_json())
    return users


def add_user(user):
    if not usuario_repository.get_user_by_email(user["user_email"]):
        usuario_repository.add_user(
            user["user_name"],
            user["user_email"],
            hashpw(user["user_password"].encode("utf-8"), gensalt()),
            user["user_birthday"],
        )
        return make_response(
            usuario_repository.get_user_by_email(user["user_email"]).to_json(), 201
        )
    else:
        return make_response(
            f'User with email {user["user_email"]} already exists', 501
        )


def get_user_by_id(user_id):
    user = usuario_repository.get_user_by_id(user_id)
    if user:
        return make_response(user.to_json(), 200)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def update_user(user_id, user):
    loaded_user = usuario_repository.get_user_by_id(user_id)
    if loaded_user:
        usuario_repository.update_user(
            user_id,
            user.get("user_name", loaded_user.nome),
            user.get("user_email", loaded_user.email),
            user.get("user_birthday", loaded_user.dt_nascimento),
        )
        return get_user_by_id(user_id)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def change_password(user_id, passwords):
    if usuario_repository.change_password(
        user_id, passwords["old_password"], passwords["new_password"]
    ):
        return make_response("Password changed sucessfully", 201)
    else:
        return make_response("Something went wrong", 501)


def delete_user(user_id):
    if usuario_repository.delete_user(user_id):
        return make_response(f"Sucessfully deleted user with id {user_id}", 204)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def get_all_events():
    return evento_repository.convert_events_to_json(
        evento_repository.Evento.select(lambda U: not U.status == 0)
    )


def add_event(event):
    user = usuario_repository.get_user_by_id(event["user_id"])
    if user:
        return make_response(
            evento_repository.add_event(
                event["name"],
                event["date"],
                event["time"],
                event["description"],
                event["notify"],
                user,
            ).to_json(),
            201,
        )
    else:
        return make_response(f'user with id {event["user_id"]} not found', 501)


def get_event_by_id(event_id):
    event = evento_repository.get_event_by_id(event_id)
    if event:
        return make_response(event.to_json(), 200)
    else:
        return make_response(f"event with id {event_id} not found", 404)


def delete_event(event_id):
    if evento_repository.delete_event(event_id):
        return make_response(f"Sucessfully deleted event with id {event_id}", 204)
    else:
        return make_response(f"event with id {event_id} not found", 404)


def update_event(event_id, event: dict):
    loaded_event = evento_repository.get_event_by_id(event_id)
    if loaded_event:
        evento_repository.update_event(
            event_id,
            event.get("name", loaded_event.nome),
            event.get("date", loaded_event.data),
            event.get("time", loaded_event.hora),
            event.get("description", loaded_event.descricao),
            event.get("notify", loaded_event.notificar),
        )
        return get_event_by_id(event_id)
    else:
        return make_response(f"Event with id {event_id} not found", 404)
