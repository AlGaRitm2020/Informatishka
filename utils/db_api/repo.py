import datetime
import asyncio
import psycopg2 as psql
from . import get_db_config_from_url


async def register(username, chat_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
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


async def add_score(task_num, result, chat_id):
    task_num = int(task_num)

    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
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

        # checking if this date for this user isn't empty
        cur.execute("SELECT right_answers FROM activity WHERE user_id = {} "
                    " AND date = '{}';".format(user_id[0][0], datetime.date.today()))
        right_answers = cur.fetchall()

        # adding activity date for user
        if not right_answers:
            cur.execute(
                "INSERT INTO activity (user_id, date, right_answers) VALUES ({}, '{}', {});".format(user_id[0][0],
                                                                                                    datetime.date.today(),
                                                                                                    1))
        else:
            cur.execute("UPDATE activity SET right_answers = '{}' WHERE user_id = '{}" \
                        "' AND date = '{}'".format(
                right_answers[0][0] + 1, user_id[0][0], datetime.date.today()))

    else:
        request = "INSERT INTO stats(user_id, task_num, right_answers, all_answers)" \
                  " VALUES({}, {}, '{}', {})".format(
            user_id[0][0], task_num, result, 1)
    cur.execute(request)
    con.commit()
    return True


async def get_activity(chat_id):
    from datetime import datetime, timedelta
    dlt = timedelta(days=7)
    date_now = datetime.now().date()

    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)
    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    request = "SELECT date, right_answers FROM activity\
    \nWHERE user_id in (SELECT id FROM users\
    \nWHERE chat_id = '{}') ORDER BY date".format(str(chat_id))
    cur.execute(request)
    result = cur.fetchall()
    if not len(result):
        return False
    items = []
    for item in result:
        date = item[0]
        if date_now + dlt >= date:
            items.append(item)
    return items


async def get_stats(chat_id, task_number=0):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    if not task_number:
        request = "SELECT task_num, right_answers, all_answers FROM stats\
        \nWHERE user_id in (SELECT id FROM users\
        \nWHERE chat_id = '{}') ORDER BY task_num".format(str(chat_id))
    else:
        request = "SELECT task_num, right_answers, all_answers FROM stats\
                \nWHERE user_id in (SELECT id FROM users\
                \nWHERE chat_id = '{}') AND task_num = {} ORDER BY task_num".format(str(chat_id), task_number)
    cur.execute(request)
    result = cur.fetchall()
    if not len(result):
        return False
    count_of_answers_dict = {}
    for task_number, right_answers, all_answers in result:
        count_of_answers_dict[str(task_number)] = (right_answers, all_answers)
    return count_of_answers_dict


async def get_all_users_chat_ids():
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    request = "SELECT chat_id FROM users"
    cur.execute(request)
    chat_ids = cur.fetchall()
    return chat_ids


if __name__ == '__main__':
    print(get_activity('1830477841'))
