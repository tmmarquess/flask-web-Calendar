from src.modules.models.Evento import *
from src.modules.models.Usuario import *
from src.modules.database.connection import db

db.generate_mapping(create_tables=True)