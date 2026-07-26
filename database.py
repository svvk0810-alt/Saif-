import sqlite3

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def setup():

    db = connect()

    cur = db.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT

    )

    """)

    db.commit()

    db.close()


def add_user(user):

    db = connect()

    cur = db.cursor()

    cur.execute("""

    INSERT OR IGNORE INTO users

    VALUES(?,?,?)

    """,(user.id,user.username,user.first_name))

    db.commit()

    db.close()


def users_count():

    db = connect()

    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM users")

    total = cur.fetchone()[0]

    db.close()

    return total