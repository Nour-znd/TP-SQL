import sqlite3

with sqlite3.connect("essai.db") as connexion:
    connexion.execute("""
        CREATE TABLE clients (
            id INTEGRER PRIMARY KEY AUTOINCREMENT,
            nom TEXT
            pays TEXT
        )
    """) 