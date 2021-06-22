import sqlite3
from datetime import datetime, timedelta

def register(username, chat_id):
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    check_request = "SELECT * FROM users WHERE chat_id = '{}'".format(str(chat_id))
    users_with_this_id = cur.execute(check_request).fetchall()
    if len(users_with_this_id):
        return False
    insert_request = "INSERT INTO users(username, chat_id) VALUES('{}', '{}')".format(username, str(chat_id))
    cur.execute(insert_request)
    con.commit()
    return True


def add_score(task_num, result, chat_id):
    date = datetime.now().date()
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    user_id = cur.execute(request).fetchall()
    if not len(user_id):
        return False
    request = "INSERT INTO stats(user_id, task_num, date, result) VALUES({}, {}, '{}', {})".format(
        user_id[0][0], task_num, date, result)
    cur.execute(request).fetchall()
    con.commit()
    return True


def get_stats(chat_id):
    dlt = timedelta(days=7)
    date_now = datetime.now().date()
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT * FROM stats\
\nWHERE user_id in (SELECT id FROM users\
\nWHERE chat_id = '{}')".format(str(chat_id))
    print(request)
    result = cur.execute(request).fetchall()
    if not len(result):
        return False
    li = []
    for item in result:
        date_list = item[3].split('-')
        date = datetime(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2])).date()
        if date_now + dlt >= date:
            li.append(item)
        print(date)
    print(li)
    all_results = {}
    for item in li:
        if item[2] not in all_results:
            all_results[item[2]] = 0
        all_results[item[2]] += item[4]
    print(all_results)
    return all_results


get_stats('906136828')
