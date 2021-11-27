from pprint import pprint

import psycopg2
import asyncio
import datetime
from utils.db_api import get_db_config_from_url

async def db_management():
    settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(settings)
    conn = psycopg2.connect(**settings.result())
    cur = conn.cursor()
    # --- drop tables ---
    """ 
    cur.execute('DROP TABLE stats;')
    cur.execute('DROP TABLE users;') 
    """
    # cur.execute('DROP TABLE activity;')
    # --- create tables ---
    """
    cur.execute("create table users(id serial primary key, username VARCHAR, chat_id  VARCHAR unique);")
    cur.execute("create table stats(id serial primary key, user_id INTEGER references users, task_num INTEGER, right_answers INTEGER, all_answers INTEGER);")
    """
    # cur.execute("create table activity(id serial primary key, user_id INTEGER references users, date DATE, right_answers INTEGER);")

    # --- insert old users ---
    """
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Joyin1211', '906136828');")
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@lelmoo', '614462421');")
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Aleksandr_Zhd', '1294053049');")
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@AlGaRitm2020', '1830477841');")
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@YulLog19', '1244102957');")
    cur.execute("INSERT INTO users (username, chat_id) VALUES ('@albert_gareev', '1283628271');")
    """
    # print(type(datetime.date.today()))
    # cur.execute("INSERT INTO activity (user_id, date, right_answers) VALUES (8, '{}', 7);".format('2021-07-07'))
    # --- delete data from tables ---
    """
    cur.execute("DELETE FROM stats;")
    cur.execute("DELETE FROM users WHERE id = 4;")
    """
    # cur.execute("DELETE FROM activity WHERE right_answers = 1;")
    # cur.execute("UPDATE stats  SET (right_answers, all_answers) =  (12, 20) WHERE user_id = 8;")
    # cur.execute("INSERT INTO stats (task_num, user_id) VALUES (3, 8);")
    # cur.execute("alter table users add column register_date DATE default '11.27.2021';")
    # --- select data from users ---
    cur.execute("SELECT * FROM users;")
    print('users', 'id, username, chat_id, register_date', sep='\n')
    pprint(cur.fetchall())

    # --- select data from stats ---
    cur.execute("SELECT * FROM stats WHERE user_id = 23;")
    print('stats', 'id, user_id, task, right_answers, all_answers', sep='\n')
    pprint(cur.fetchall())

    # --- select data from users ---
    cur.execute("SELECT * FROM activity;")
    print('id', 'user_id, date', sep='\n')
    pprint(cur.fetchall())

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(db_management())
