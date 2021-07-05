import psycopg2 as psql
from get_db_config_from_url import get_db_config_from_url


def register(username, chat_id):
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    check_request = "SELECT * FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(check_request)
    users_with_this_id = cur.fetchall()
    if len(users_with_this_id):
        return False
    insert_request = "INSERT INTO users(username, chat_id) VALUES('{}', '{}')". \
        format(username, str(chat_id))
    cur.execute(insert_request)
    con.commit()
    return True


def add_score(task_num, result, chat_id):
    task_num = int(task_num)
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(request)
    user_id = cur.fetchall()
    if not len(user_id):
        return False
    check_request = "SELECT right_answers, all_answers FROM stats WHERE user_id = '{}'" \
                    " AND task_num = '{}'".format(
        user_id[0][0], task_num)
    cur.execute(check_request)
    results = cur.fetchall()
    if len(results):
        request = "UPDATE stats SET right_answers = '{}', all_answers = '{}' WHERE user_id = '{}" \
                  "' AND task_num = '{}'".format(
            results[0][0] + result, results[0][1] + 1, user_id[0][0], task_num)
    else:
        request = "INSERT INTO stats(user_id, task_num, right_answers, all_answers)" \
                  " VALUES({}, {}, '{}', {})".format(
            user_id[0][0], task_num, result, 1)
    cur.execute(request)
    con.commit()
    return True


def get_stats(chat_id):
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT task_num, right_answers, all_answers FROM stats\
\nWHERE user_id in (SELECT id FROM users\
\nWHERE chat_id = '{}') ORDER BY task_num".format(str(chat_id))
    cur.execute(request)
    result = cur.fetchall()
    if not len(result):
        return False
    count_of_answers_dict = {}
    for task_number, right_answers, all_answers in result:
        count_of_answers_dict[str(task_number)] = (right_answers, all_answers)
    return count_of_answers_dict


def get_all_users_chat_ids():
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT chat_id FROM users"
    cur.execute(request)
    chat_ids = cur.fetchall()
    return chat_ids


if __name__ == '__main__':
    print(get_stats('1830477841'))
