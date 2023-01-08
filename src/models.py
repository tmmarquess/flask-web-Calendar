from pony.orm import Database, Required, Optional, PrimaryKey
from flask_login import UserMixin
from datetime import date

db = Database()
db.bind(provider="sqlite", filename="calendar.db", create_db=True)


class Usuario(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    nome = Required(str)
    senha = Required(str)
    dt_nascimento = Required(date)
    status = Required(int)


class Evento(db.Entity):
    id = PrimaryKey(int, auto=True)


db.generate_mapping(create_tables=True)
