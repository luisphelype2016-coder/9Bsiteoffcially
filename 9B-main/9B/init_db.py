import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS assuntos (

id INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT,
texto TEXT,
autor TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS atividades (

id INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT,
texto TEXT,
autor TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grupos (

id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT,
participantes TEXT,
criador TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mensagens (

id INTEGER PRIMARY KEY AUTOINCREMENT,
grupo_id INTEGER,
autor TEXT,
mensagem TEXT

)
""")

conn.commit()
conn.close()

import sqlite3
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE mensagens ADD COLUMN datahora TEXT")

conn.commit()
conn.close()

print("Banco criado com sucesso")