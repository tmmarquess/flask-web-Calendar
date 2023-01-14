from pony.orm import Database

db = Database()
# db.bind(provider="sqlite", filename="../../calendar.db", create_db=True)

db.bind(
    provider="mysql",
    user="PonyCalendar",
    passwd="pony123",
    host="127.0.0.1",
    db="calendar",
)
