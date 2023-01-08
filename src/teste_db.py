import sqlite3

connection = sqlite3.connect('calendar.db')
cursor = connection.cursor()

cursor.execute("select * from Usuario")
print(cursor.fetchall())