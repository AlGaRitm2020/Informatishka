import matplotlib.pyplot as plt
import os


async def reformat_to_dd_mm_yyyy(date: str) -> str:
    yyyy_mm_dd_list = date.split('-')
    dd_mm_yyyy_list = [yyyy_mm_dd_list[2], yyyy_mm_dd_list[1], yyyy_mm_dd_list[0]]
    dd_mm_yyy_str = '.'.join(dd_mm_yyyy_list)
    return dd_mm_yyy_str[:-5]


async def get_user_activity_diagram(dates_and_answers_stats):
    dates_and_answers_stats = dates_and_answers_stats[-10:] 
    dates = [await reformat_to_dd_mm_yyyy(str(i[0])) for i in dates_and_answers_stats]
    answers = [i[1] for i in dates_and_answers_stats]
    fig, ax = plt.subplots()

    ax.set_title(f"Статистика по активности", fontsize=20)
    ax.set_xlabel('Дата')
    ax.set_ylabel('Решено задач')
    ax.bar(dates, answers)
    plt.savefig('data/temp_task_files/activity.png')
    byte_img = open('data/temp_task_files/activity.png', mode='rb').read()
    plt.close()
    return byte_img
