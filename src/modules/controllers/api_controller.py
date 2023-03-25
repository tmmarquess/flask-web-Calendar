import src.modules.database.evento_repository as evento_repository
import src.modules.database.usuario_repository as usuario_repository
from flask_login import current_user, login_required, logout_user
from src.resources.app import authenticate_user
from bcrypt import hashpw, gensalt, checkpw
from flask import make_response


def __is_current_user_authenticated():
    try:
        current_user.to_json()
        return True
    except AttributeError:
        return False


def login(credentials):
    if authenticate_user(credentials["email"], credentials["password"]):
        return make_response("Sucessfully Login", 201)
    else:
        return make_response("wrong credentials", 501)


def logout():
    try:
        current_user.set_authenticated(False)
        logout_user()
        return make_response("Sucessfully Logout", 200)
    except AttributeError:
        return make_response("There is no user active in this session", 501)


def get_all_users():
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
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
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    user = usuario_repository.get_user_by_id(user_id)
    if user:
        return make_response(user.to_json(), 200)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def update_user(user_id, user):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    loaded_user = usuario_repository.get_user_by_id(user_id)
    if loaded_user:
        print(current_user.id)
        print(user_id)
        if current_user.id == int(user_id):
            usuario_repository.update_user(
                user_id,
                user.get("user_name", loaded_user.nome),
                user.get("user_email", loaded_user.email),
                user.get("user_birthday", loaded_user.dt_nascimento),
            )
            return get_user_by_id(user_id)
        else:
            return make_response("You can only edit the currently active user", 501)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def change_password(user_id, passwords):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    if current_user.id == int(user_id) and usuario_repository.change_password(
        user_id, passwords["old_password"], passwords["new_password"]
    ):
        return make_response("Password changed sucessfully", 201)
    else:
        return make_response("Something went wrong", 501)


def delete_user(user_id):  #  MODIFICAR
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    if current_user.id == int(user_id) and usuario_repository.delete_user(user_id):
        return make_response(f"Sucessfully deleted user with id {user_id}", 204)
    else:
        return make_response(f"User with id {user_id} not found", 404)


def get_all_events():
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    return evento_repository.convert_events_to_json(
        evento_repository.Evento.select(lambda U: not U.status == 0)
    )


def add_event(event):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    return make_response(
        evento_repository.add_event(
            event["name"],
            event["date"],
            event["time"],
            event["description"],
            event["notify"],
            current_user,
        ).to_json(),
        201,
    )


def get_user_events(user_id):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    if current_user.id != user_id:
        return make_response("You can only get your events", 501)
    return make_response(evento_repository.get_all_user_events(user), 200)


def get_event_by_id(event_id):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    event = evento_repository.get_event_by_id(event_id)
    if event:
        return make_response(event.to_json(), 200)
    else:
        return make_response(f"event with id {event_id} not found", 404)


def delete_event(event_id):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)

    if current_user.id != evento_repository.get_event_by_id(event_id).usuario.id:
        return make_response(
            "You can only delete events of the currently active user", 501
        )
    if evento_repository.delete_event(event_id):
        return make_response(f"Sucessfully deleted event with id {event_id}", 204)
    else:
        return make_response(f"event with id {event_id} not found", 404)


def update_event(event_id, event: dict):
    if not __is_current_user_authenticated():
        return make_response("Authentication Required", 505)
    loaded_event = evento_repository.get_event_by_id(event_id)
    if current_user.id != loaded_event.usuario.id:
        return make_response(
            "You can only edit events from the currently active user", 501
        )
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
