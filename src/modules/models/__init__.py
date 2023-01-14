from modules.models.Evento import *
from modules.models.Usuario import *
from modules.database.connection import db

db.generate_mapping(create_tables=True)