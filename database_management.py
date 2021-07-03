from pprint import pprint

from config import DB_HOST, DB_NAME, DB_USER, DB_PASS
import psycopg2

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host= DB_HOST)

cur = conn.cursor()

# --- drop tables ---
""" 
cur.execute('DROP TABLE stats;')
cur.execute('DROP TABLE users;') 
"""

# --- create tables ---
"""
cur.execute("create table users(id serial primary key, username VARCHAR, chat_id  VARCHAR unique);")
cur.execute("create table stats(id serial primary key, user_id INTEGER references users, task_num INTEGER, right_answers INTEGER, all_answers INTEGER);")
"""

# --- insert old users ---
"""
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Joyin1211', '906136828');")
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@lelmoo', '614462421');")
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Aleksandr_Zhd', '1294053049');")
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@AlGaRitm2020', '1830477841');")
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@YulLog19', '1244102957');")
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@albert_gareev', '1283628271');")
"""

# --- delete data from tables ---
"""
cur.execute("DELETE FROM stats;")
cur.execute("DELETE FROM users WHERE id = 4;")
"""

# --- select data from users ---
cur.execute("SELECT * FROM users;")
print('users', 'id, username, chat_id', sep='\n')
pprint(cur.fetchall())

# --- select data from stats ---
cur.execute("SELECT * FROM stats;")
print('stats', 'id, user_id, task, right_answers, all_answers', sep='\n')
pprint(cur.fetchall())


conn.commit()
cur.close()
conn.close()
