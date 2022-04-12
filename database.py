import sqlite3
from datetime import datetime

def connect_to_db():
    conn = sqlite3.connect('db')
    return conn


def create_db_table():
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


def insert_user(user, currentTime):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND end_log=?", (user['name'],0,))
        row = cur.fetchone()
        if row is not None:
            isInserted = False#response output should be user cant start new task previous is not done
        else: #if row none it means there is no user in the table with that name/first task for that user
            #if found user but it's end_log isn't zero,it means user finished previous task and need to insert new task
            cur.execute("INSERT INTO users (name, task, start_log, end_log) VALUES (?,?,?,?)",
                        (user['name'], user['task'], currentTime, 0))
            isInserted = True
        conn.commit()
    except Exception as e:
        print(e)
        conn().rollback()

    finally:
        conn.close()

    return isInserted


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
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["task"] = i["task"]
            if i["end_log"] != None and i["start_log"] != None:
                endTime = datetime.strptime(i["end_log"], "%H:%M")
                startTime = datetime.strptime(i["start_log"], "%H:%M")
                totalTimeStr = str(endTime - startTime)
                user["total_work_time(%H:%M:%S)"] = totalTimeStr
            users.append(user)

    except Exception as e:
        print(e)
        users = []

    return users


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?",
                    (user_id,))
        row = cur.fetchone()

        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["task"] = row["task"]
        if row["end_log"] != None and row["start_log"] != None:
            endTime = datetime.strptime(row["end_log"], "%H:%M")
            startTime = datetime.strptime(row["start_log"], "%H:%M")
            totalTimeStr = str(endTime - startTime)
            user["total_work_time(%H:%M:%S)"] = totalTimeStr
    except Exception as e:
        print(e)
        user = {}

    return user


def update_user(user, currentTime):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND end_log=?", (user['name'], 0,))
        row = cur.fetchone()
        if row is not None:
            cur.execute("UPDATE users SET end_log = ? "
                        "WHERE user_id =?",
                        (currentTime, row[0],))
            isUpdated = True
        else:
            isUpdated = False
        conn.commit()


    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

    return isUpdated
