import sqlite3

DB_PATH = "people.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            photo_path TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def save_person(name, age, photo_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO people (name, age, photo_path) VALUES (?, ?, ?)
    """,
        (name, age, photo_path),
    )
    conn.commit()
    conn.close()


def get_people():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    results = cursor.fetchall()
    conn.close()
    return results
