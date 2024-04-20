import sqlite3
from config import DB_PATH


def is_unique_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("select id from user;")
    results = cur.fetchall()
    if user_id in [el for a_list in results for el in a_list]:
        return False # если id пользователя уже записано в бд
    else:
        return True


def insert_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO user(id) VALUES({user_id});")
    conn.commit()


def push_inf(credit, instant_rate, months, user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"UPDATE user SET Pv={credit}, Ry={instant_rate}, Ly={months} WHERE id={user_id}")
    conn.commit()


def check_inf():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("select * from user;")
    results = cur.fetchall()
    return results


def get_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"select Pv, Ry, Ly from user where id = {user_id};")
    data = cur.fetchall()[0]
    if data[0] is None:
        return None
    else:
        return data


def change_prmtr(user_id, prmtr, arg):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"UPDATE user SET {prmtr}={arg}")
    conn.commit()


def delete_table_inf(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM user WHERE id = {user_id};")
    conn.commit()
