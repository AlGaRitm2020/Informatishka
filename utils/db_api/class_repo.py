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


async def view_class(class_id, chat_id, read_only=False):
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
    if teacher_id[0][0] == student_id and read_only == False:
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
    select_request = "SELECT id, name FROM classes WHERE teacher_id = '{}'".format(user_id)
    cur.execute(select_request)
    classes_info = cur.fetchall()

    select_request = "SELECT id, name FROM classes WHERE id IN (SELECT class_id FROM classmates WHERE user_id = '{}')".format(user_id)
    cur.execute(select_request)
    classes_info = classes_info + cur.fetchall()

    con.commit()
    return classes_info

async def leave_from_class(class_id, chat_id):
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


    cur.execute("DELETE FROM classmates WHERE user_id = '{}' AND class_id = '{}'".format(user_id, class_id))
    con.commit()
    

async def delete_class(class_id, chat_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    cur.execute("DELETE FROM classmates WHERE class_id = '{}'".format(class_id))
    cur.execute("DELETE FROM classes WHERE id = '{}'".format(class_id))
    con.commit()
 
async def remove_student(class_id, student_name):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    cur.execute("DELETE FROM classmates WHERE class_id = '{}' AND name = '{}'".format(class_id, student_name))
    con.commit()

async def view_class_members(class_id, teacher=True):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    select_request = "SELECT name FROM classmates WHERE class_id = '{}'".format(class_id)
    cur.execute(select_request)

    members_list = cur.fetchall()
    if teacher:
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

async def get_student_chat_id(class_id, student_name):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT chat_id FROM users WHERE id in (SELECT user_id from classmates WHERE name = '{}' AND class_id = '{}')".format(student_name, class_id)
    cur.execute(check_request)
    user = cur.fetchall()
    if not user:
        return False
    chat_id = user[0][0]

    return chat_id 



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
   





#=====HOMEWORKS_BLOCK=====

async def create_homework(name, class_id, tasks):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    insert_request = "INSERT INTO homeworks(class_id, name, tasks, date, is_open) VALUES('{}', '{}', '{}', '{}', '{}' )". \
        format(class_id, name, tasks, datetime.date.today(), 1)
    cur.execute(insert_request)
    con.commit()

async def get_homeworks(class_id):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT name, tasks FROM homeworks WHERE class_id = '{}'".format(class_id)
    cur.execute(check_request)
    homeworks = cur.fetchall()

    return homeworks 


async def get_work_info(class_id, work_name):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()
    check_request = "SELECT date, is_open FROM homeworks WHERE class_id = '{}' AND name = '{}'".format(class_id, work_name)
    cur.execute(check_request)
    work_info = cur.fetchall()[0]

    return work_info 



async def change_work_status(class_id, work_name):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    check_request = "SELECT is_open FROM homeworks WHERE class_id = '{}' AND name = '{}'".format(class_id, work_name)
    cur.execute(check_request)
    status = cur.fetchall()[0][0]
    if status == 0:
        new_status = 1
    else:
        new_status = 0
    update_request = "UPDATE homeworks SET is_open = '{}'".format(new_status)
    cur.execute(update_request)

    con.commit()
    
    return new_status



async def delete_work(class_id, work_name):
    db_settings = asyncio.create_task(get_db_config_from_url())
    await asyncio.gather(db_settings)

    con = psql.connect(**db_settings.result())
    cur = con.cursor()

    delete_request = "DELETE FROM homeworks WHERE class_id = '{}' AND name = '{}'".format(class_id, work_name)
    cur.execute(delete_request)
    con.commit()
    
