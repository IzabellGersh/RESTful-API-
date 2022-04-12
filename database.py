import sqlite3
from datetime import datetime


def connect_to_db():
    conn = sqlite3.connect('db')
    return conn


def create_db_table():
    conn = connect_to_db()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                task TEXT NOT NULL,
                start_log TIMESTAMP,
                end_log TIMESTAMP
            );
        ''')

        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(e)
        print("User table creation failed - Maybe table")
    finally:
        conn.close()


def insert_user(user, current_time):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND end_log=?", (user['name'], 0,))
        row = cur.fetchone()
        if row is not None:
            is_inserted = False  # response output should be user can't start new task previous is not done
        else:  # if row none it means there is no user in the table with that name/first task for that user
            # if found user, but it's end_log isn't zero,it means user finished previous task and need to insert new task
            cur.execute("INSERT INTO users (name, task, start_log, end_log) VALUES (?,?,?,?)",
                        (user['name'], user['task'], current_time, 0))
            is_inserted = True
        conn.commit()
    except Exception as e:
        print(e)
        is_inserted = False
        conn().rollback()

    finally:
        conn.close()

    return is_inserted


def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {"user_id": i["user_id"], "name": i["name"], "task": i["task"]}
            if i["end_log"] is not None and i["start_log"] is not None:
                end_time = datetime.strptime(i["end_log"], "%H:%M")
                start_time = datetime.strptime(i["start_log"], "%H:%M")
                total_time_str = str(end_time - start_time)
                user["total_work_time(%H:%M:%S)"] = total_time_str
            users.append(user)

    except Exception as e:
        print(e)
        users = []

    return users


def update_user(user, current_time):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND end_log=?", (user['name'], 0,))
        row = cur.fetchone()
        if row is not None:
            cur.execute("UPDATE users SET end_log = ? "
                        "WHERE user_id =?",
                        (current_time, row[0],))
            is_updated = True
        else:
            is_updated = False
        conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()
        is_updated = False
    finally:
        conn.close()

    return is_updated
