import sqlite3


def register(username, chat_id):
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT * FROM users\
\nWHERE chat_id = '{}'".format(str(chat_id))
    usrs_with_id = cur.execute(request).fetchall()
    if len(usrs_with_id):
        return False
    request = "INSERT INTO users(username, chat_id)\
\nVALUES('{}', '{}')".format(username, str(chat_id))
    cur.execute(request).fetchall()
    con.commit()
    return True


def add_score(task_num, result, chat_id):
    from datetime import datetime
    date = datetime.now().date()
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT id FROM users\
\nWHERE chat_id = '{}'".format(str(chat_id))
    user_id = cur.execute(request).fetchall()
    if not len(user_id):
        return False
    request = "INSERT INTO stats(user_id, task_num, date, result)\
\nVALUES({}, {}, '{}', {})".format(user_id[0][0], task_num, date, result)
    cur.execute(request).fetchall()
    con.commit()
    return True


def get_stats(chat_id):
    from datetime import datetime, timedelta
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
    nice_dick = []
    for item in result:
        date_list = item[3].split('-')
        date = datetime(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2])).date()
        if date_now + dlt >= date:
            nice_dick.append(item)
        print(date)
    print(nice_dick)
    all_results = {}
    for item in nice_dick:
        if item[2] not in all_results:
            all_results[item[2]] = 0
        all_results[item[2]] += item[4]
    print(all_results)
    return all_results


get_stats('906136828')
