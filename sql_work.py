import sqlite3

def register(username, chat_id):
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    check_request = "SELECT * FROM users WHERE chat_id = '{}'".format(str(chat_id))
    users_with_this_id = cur.execute(check_request).fetchall()
    if len(users_with_this_id):
        return False
    insert_request = "INSERT INTO users(username, chat_id) VALUES('{}', '{}')".\
        format(username, str(chat_id))
    cur.execute(insert_request)
    con.commit()
    return True


def add_score(task_num, result, chat_id):
    task_num = int(task_num)
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    user_id = cur.execute(request).fetchall()
    if not len(user_id):
        return False
    check_request = "SELECT right_answers, all_answers FROM stats WHERE user_id = '{}'" \
                    " AND task_num = '{}'".format(
        user_id[0][0], task_num)
    results = cur.execute(check_request).fetchall()[0]
    if len(results):
        request = "UPDATE stats SET right_answers = '{}', all_answers = '{}' WHERE user_id = '{}" \
                  "' AND task_num = '{}'".format(
            results[0] + result, results[1] + 1, user_id[0][0], task_num)
    else:
        request = "INSERT INTO stats(user_id, task_num, right_answers, all_answers)" \
                  " VALUES({}, {}, '{}', {}, {})".format(
            user_id[0][0], task_num, result, 1)
    cur.execute(request)
    con.commit()
    return True


def get_stats(chat_id):

    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT task_num, right_answers, all_answers FROM stats\
\nWHERE user_id in (SELECT id FROM users\
\nWHERE chat_id = '{}')".format(str(chat_id))
    result = cur.execute(request).fetchall()
    if not len(result):
        return False
    count_of_answers_dict = {}
    for task_number, right_answers, all_answers in result:
        count_of_answers_dict[str(task_number)] = (right_answers, all_answers)
    return count_of_answers_dict

print(get_stats('1830477841'))
