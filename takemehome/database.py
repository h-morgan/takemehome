import sqlite3
from loguru import logger
import os
import appdirs

APP_NAME = "Take Me Home"
db_dir = appdirs.user_data_dir(APP_NAME)  # Resolves to a system-specific directory
os.makedirs(db_dir, exist_ok=True)  # Ensure the directory exists
db_path = os.path.join(db_dir, "people.db")  # Store DB here

logger.debug(f"Database path: {db_path}")

# Check if the database exists, if not, create it
if not os.path.exists(db_path):
    # Create a connection to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    # You could also create tables or perform other setup tasks here
    conn.close()


def init_db():
    conn = sqlite3.connect(db_path)
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
        "race": "TEXT",
        "sex": "TEXT",
        "height": "INTEGER",
        "weight": "INTEGER",
        "street": "TEXT",
        "city": "TEXT",
        "state": "TEXT",
        "zipcode": "INTEGER",
        "special_bracelet_id": "TEXT",
        "organization": "TEXT",
        "record_type": "TEXT",
        "picture_date": "TEXT",
        "age_in_picture": "INTEGER",
        "photo_path": "TEXT",
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
    INSERT INTO people (name_to_call_me, first_name, middle_name, last_name, dob, age, hair, eyes, race, sex, height, weight, street, city, state, zipcode, special_bracelet_id, organization, record_type, picture_date, age_in_picture, photo_path)
    VALUES (:name_to_call_me, :first_name, :middle_name, :last_name, :dob, :age, :hair, :eyes, :race, :sex, :height, :weight, :street, :city, :state, :zipcode, :special_bracelet_id, :organization, :record_type, :picture_date, :age_in_picture, :photo_path)
    """,
        person_data,
    )

    conn.commit()
    conn.close()


def search_people(dob=None, race=None, sex=None, hair=None, eyes=None):
    conn = sqlite3.connect("people.db")
    cursor = conn.cursor()

    query = """
    SELECT name_to_call_me, first_name, middle_name, last_name, dob, age, hair, eyes, race, sex, height, weight, street, city, state, zipcode, special_bracelet_id, organization, record_type, picture_date, age_in_picture, photo_path
    FROM people
    where first_name != ''
    """
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
        params.append(hair)
    if eyes:
        query += " AND eyes LIKE ?"
        params.append(eyes)

    logger.debug(query)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results
