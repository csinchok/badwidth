import datetime
import sqlite3

CREATION_SQL = '''
CREATE TABLE stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp DATETIME NOT NULL,
    stat VARCHAR(64) NOT NULL,
    value REAL NOT NULL,
    unit VARCHAR(10) NOT NULL
)
'''


def create(conn):
    # Creates a database and schema
    c = conn.cursor()

    for line in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stats';"):
        break
    else:
        c.execute(CREATION_SQL)
        conn.commit()



def save_stats(conn, stats=None):
    stats = stats or []

    c = conn.cursor()

    timestamp = datetime.now()

    for stat, value, unit in stats:
        c.execute('INSERT INTO stats (timestamp, stat, value, unit) VALUES (?, ?, ?, ?)', [
            timestamp, stat, value, unit
        ])

    conn.commit()
