import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

with open("database/schema.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Banco criado com sucesso!")