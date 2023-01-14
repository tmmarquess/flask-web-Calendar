from modules.database.connection import db
from modules.models.Usuario import Usuario
from pony.orm import Required, PrimaryKey
from datetime import date


class Evento(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    data = Required(date)
    hora = Required(str)
    descricao = Required(str)
    notificar = Required(bool)
    status = Required(int)
    usuario = Required(Usuario)
