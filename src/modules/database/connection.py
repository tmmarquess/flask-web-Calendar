from pony.orm import Database

db = Database()
db.bind(provider="sqlite", filename="../../calendar.db", create_db=True)