from modules.database.connection import db
from modules.models.Usuario import Usuario
from pony.orm import Required, PrimaryKey
from datetime import datetime


class Evento(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    dt_hr_inicio = Required(datetime)
    dt_hr_fim = Required(datetime)
    descricao = Required(str)
    notificar = Required(bool)
    status = Required(int)
    usuario = Required(Usuario)
