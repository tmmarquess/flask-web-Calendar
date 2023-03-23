from src.modules.database.connection import db
from src.modules.models.Usuario import Usuario
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

    def to_json(self):
        return dict(
            id=self.id,
            name=self.nome,
            date=self.data,
            day=self.data.day,
            month=self.data.month,
            year=self.data.year,
            time=self.hora,
            description=self.descricao,
            notify=self.notificar,
            status=self.status,
            usuario=self.usuario.id,
        )
