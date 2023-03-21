from src.modules.database.connection import db
from pony.orm import Required, PrimaryKey, Set
from flask_login import UserMixin
from datetime import date


class Usuario(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    nome = Required(str)
    senha = Required(bytes)
    dt_nascimento = Required(date)
    status = Required(int)
    eventos = Set("Evento")
    __is_authenticated = Required(bool, default=False)

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    def is_active(self):
        return self.is_authenticated

    def is_anonymous(self):
        return super().is_anonymous

    def get_id(self):
        return super().get_id()

    def set_authenticated(self, value: bool):
        self.__is_authenticated = value

    def to_json(self):
        return dict(
            id=self.id,
            email=self.email,
            nome=self.nome,
            dt_nascimento=self.dt_nascimento,
            status=self.status,
        )
