import datetime
import asyncio
import logging

import psycopg2 as psql
from . import get_db_config_from_url


async def create_class(class_name, teacher_name, chat_id):
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

    insert_request = "INSERT INTO classes(teacher_id, name, teacher_name) VALUES('{}', '{}', '{}' )". \
        format(user_id, class_name, teacher_name)
    cur.execute(insert_request)
    con.commit()

    cur.execute("SELECT id FROM classes WHERE teacher_id = '{}' AND name = '{}';".format(user_id, class_name))
    class_id = cur.fetchall()[0][0]


    return class_id


async def view_class(class_id, chat_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(check_request)
    user = cur.fetchall()
    if not user:
        return False
    student_id = user[0][0]


    check_request = "SELECT teacher_id FROM classes WHERE id = '{}'".format(class_id)
    cur.execute(check_request)
    teacher_id = cur.fetchall()
    if not teacher_id:
        return "Класс с таким id не существует"
    if teacher_id[0][0] == student_id:
        return "Вы уже являетесь учителем в этом классе"


    check_request = "SELECT name FROM classmates WHERE user_id = '{}' AND class_id = '{}'".format(student_id, class_id)
    cur.execute(check_request)
    is_registred = cur.fetchall()
    if is_registred:
        return f"Вы уже являетесь учеником в этом классе под именем {is_registred[0][0]}"


    select_request = "SELECT name, teacher_name FROM classes WHERE id = '{}'".format(class_id)
    cur.execute(select_request)

    class_info = cur.fetchall()[0] 
    con.commit()
    return class_info


async def view_all_user_classes(chat_id):
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


    select_request = "SELECT classes.id, classes.name FROM classes, classmates WHERE classmates.user_id = '{}' OR classes.teacher_id = '{}'".format(user_id, user_id)
    cur.execute(select_request)

    classes_info = cur.fetchall()
    con.commit()
    return classes_info




async def view_class_members(class_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    select_request = "SELECT name FROM classmates WHERE class_id = '{}'".format(class_id)
    cur.execute(select_request)

    members_list = cur.fetchall()

    select_request = "SELECT teacher_name FROM classes WHERE id = '{}'".format(class_id)
    cur.execute(select_request)
    
    members_list = cur.fetchall() + members_list

    con.commit()
    return members_list 



async def is_teacher(class_id, chat_id):
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

    select_request = "SELECT teacher_id FROM classes WHERE teacher_id = '{}' AND id = '{}'".format(user_id, class_id)
    cur.execute(select_request)

    is_teacher = cur.fetchall()
    return bool(is_teacher)



async def join_class(class_id, student_name, chat_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(check_request)
    user = cur.fetchall()
    if not user:
        return False
    student_id = user[0][0]






    


    check_request = "SELECT name FROM classmates WHERE class_id = '{}' AND name = '{}'".format(class_id, student_name)
    cur.execute(check_request)
    is_name_exists = cur.fetchall()
    if is_name_exists:
        return "Ученик с таким именем уже зарегистрирован в этом классе\nВыберите другое имя"



    insert_request = "INSERT INTO classmates(user_id, class_id, name) VALUES('{}', '{}', '{}' )". \
        format(student_id, class_id, student_name)
    cur.execute(insert_request)
    con.commit()
    
