from pprint import pprint
from bs4 import BeautifulSoup
import requests
import random
from task_text_parser import get_task_text
import json


def get_task_by_number(task_number):
    """This function return task, answer and extra files like images, excel, word"""
    # get dict from json
    with open("categories.json", "r") as categories:
        categories_dict = json.load(categories)

    category = categories_dict[task_number]
    url = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={task_number}&{category}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    center = soup.find('div', class_='center')
    tasks_count = int(str(center.findAll('p')[1])[20:22])
    tasks_table = center.find('table', class_='vartopic')
    random_task = random.randint(0, tasks_count - 1)

    answer = tasks_table.findAll('tr')[1::2][random_task]
    task_tr = tasks_table.findAll('tr')[::2][random_task]
    task_td = task_tr.find('td', class_='topicview')
    task_script = task_td.find('script')
    task_script_text = str(task_script)
    # making img_addresses list

    if 'img' in task_script_text:
        begin_index = task_script_text.find('img') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        img_address = task_script_text[begin_index:end_index]
    else:
        img_address = None

    # making answers list
    answer = answer.find('script')
    script_txt = str(answer)
    left_border_index = script_txt.find("'") + 1
    right_border_index = script_txt.rfind("'")
    answer = [script_txt[left_border_index:right_border_index]]

    # making excel_files list
    if '<a' in task_script_text and 'xls' in task_script_text:
        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        excel_address = task_script_text[begin_index:end_index]
    else:
        excel_address = None

    # making word_files list
    if '<a' in task_script_text and 'docx' in task_script_text:
        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        word_address = task_script_text[begin_index:end_index]
    else:
        word_address = None

    result_task = get_task_text(task_script)

    return result_task, answer, img_address, excel_address, word_address


get_task_by_number('6')
