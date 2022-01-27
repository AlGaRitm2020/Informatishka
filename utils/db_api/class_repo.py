import datetime
import asyncio
import logging

import psycopg2 as psql
from . import get_db_config_from_url


async def create_class(class_name, chat_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(check_request)
    user = cur.fetchall()
    if not user:
        return False
    user_id = user[0][0]

    insert_request = "INSERT INTO classes(teacher_id, name) VALUES('{}', '{}' )". \
        format(user_id, class_name)
    cur.execute(insert_request)
    con.commit()

    cur.execute("SELECT id FROM classes WHERE teacher_id = '{}';".format(user_id))
    class_id = cur.fetchall()[0][0]


    return class_id
