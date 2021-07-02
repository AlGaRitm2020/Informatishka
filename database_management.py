DB_HOST = 'ec2-54-228-9-90.eu-west-1.compute.amazonaws.com'
DB_NAME = 'd2gkvsrqqt4jjg'
DB_USER = 'tkdhlpgcbebdlg'
DB_PASS = 'cd7765e4f10eded0fecddd174a1b19e21cbb8cf6957c21289d8fd774f63efd91'

import psycopg2

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host= DB_HOST)

cur = conn.cursor()
# cur.execute('DROP TABLE stats;')
# cur.execute('DROP TABLE users;')
#
# cur.execute("create table users(id serial primary key, username VARCHAR, chat_id  VARCHAR unique);")
# cur.execute("create table stats(id serial primary key, user_id INTEGER references users, task_num INTEGER, right_answers INTEGER, all_answers INTEGER);")
#
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Joyin1211', '906136828');")
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@lelmoo', '614462421');")
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@Aleksandr_Zhd', '1294053049');")
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@AlGaRitm2020', '1830477841');")
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@YulLog19', '1244102957');")
# cur.execute("INSERT INTO users (username, chat_id) VALUES ('@albert_gareev', '1283628271');")
# cur.execute("DELETE FROM users WHERE id = 1;")
cur.execute("SELECT * FROM stats;")
# cur.execute("INSERT INTO student (name) values(%s)", ("Albert",))
# cur.execute("DROP TABLE student;")
print(cur.fetchall())
conn.commit()

cur.close()

conn.close()
