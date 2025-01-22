import sqlite3


def init_db():
    conn = sqlite3.connect("people.db")
    cursor = conn.cursor()

    # Desired schema for the "people" table
    desired_columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "first_name": "TEXT",
        "middle_name": "TEXT",
        "last_name": "TEXT",
        "name_to_call_me": "TEXT",
        "dob": "TEXT",
        "age": "INTEGER",
        "hair": "TEXT",
        "eyes": "TEXT",
    }

    # Ensure the table exists
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
    """
    )

    # Get current schema
    cursor.execute("PRAGMA table_info(people)")
    existing_columns = {col[1]: col[2] for col in cursor.fetchall()}

    # Add missing columns
    for column, column_type in desired_columns.items():
        if column not in existing_columns:
            cursor.execute(f"ALTER TABLE people ADD COLUMN {column} {column_type}")
        elif column == "id" and existing_columns[column] == "INTEGER":
            # Skip warning for 'id' as SQLite internally manages PRIMARY KEY AUTOINCREMENT
            continue
        elif existing_columns[column] != column_type:
            print(
                f"Warning: Column '{column}' exists with type '{existing_columns[column]}' but expected '{column_type}'."
            )

    conn.commit()
    conn.close()


def add_person(person_data):
    conn = sqlite3.connect("people.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO people (name_to_call_me, first_name, middle_name, last_name, dob, age, hair, eyes)
    VALUES (:name_to_call_me, :first_name, :middle_name, :last_name, :dob, :age, :hair, :eyes)
    """,
        person_data,
    )

    conn.commit()
    conn.close()


def search_people(dob=None, race=None, sex=None, hair=None, eyes=None):
    conn = sqlite3.connect("people.db")
    cursor = conn.cursor()

    query = "SELECT * FROM people WHERE 1=1"
    params = []

    if dob:
        query += " AND dob = ?"
        params.append(dob)
    if race:
        query += " AND race = ?"
        params.append(race)
    if sex:
        query += " AND sex = ?"
        params.append(sex)
    if hair:
        query += " AND hair LIKE ?"
        params.append(f"%{hair}%")
    if eyes:
        query += " AND eyes LIKE ?"
        params.append(f"%{eyes}%")

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results
