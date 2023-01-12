import sqlite3

connection = sqlite3.connect('calendar.db')
cursor = connection.cursor()

cursor.execute("select * from Usuario")
print(cursor.fetchall())

cursor.execute("select * from Evento")
print(cursor.fetchall())