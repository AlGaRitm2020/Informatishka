import sqlite3


def register(username, chat_id):
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    request = "SELECT * FROM users\
WHERE chat_id={}".format(str(chat_id))
    usrs_with_id = cur.execute(request).fetchall()
    if len(usrs_with_id):
        return False
    request = "INSERT INTO users(username, chat_id)\
'\n'VALUES({}, {})".format(username, str(chat_id))
    return True


def add_score():
    pass


def get_stats():
    pass

