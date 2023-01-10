from pony.orm import Database, Required, Optional, PrimaryKey, Set
from flask_login import UserMixin
from datetime import date, datetime

db = Database()
db.bind(provider="sqlite", filename="calendar.db", create_db=True)


class Usuario(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    nome = Required(str)
    senha = Required(str)
    dt_nascimento = Required(date)
    status = Required(int)
    eventos = Set("Evento")
    is_authenticated = Required(bool, default=False)

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_authenticated

    def is_anonymous(self):
        return super().is_anonymous

    def get_id(self):
        return super().get_id()


class Evento(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    dt_hr_inicio = Required(datetime)
    dt_hr_fim = Required(datetime)
    descricao = Required(str)
    notificar = Required(bool)
    status = Required(int)
    usuario = Required(Usuario)


db.generate_mapping(create_tables=True)
