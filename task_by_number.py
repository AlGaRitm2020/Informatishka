from bs4 import BeautifulSoup
import requests
import random

from get_files import get_excel, get_photo, get_word
from task_text_parser import get_task_text
import json


def get_task_by_number(task_number):
    """This function return task, answer and extra files like images, excel, word"""
    if 20 <= int(task_number) <= 21:
        task_number = '19'
    # get dict from json
    with open("data/categories.json", "r") as categories:
        categories_dict = json.load(categories)

    category = categories_dict[task_number]
    url = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=' \
          f'{task_number}&{category}'
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
        byte_img = get_photo(img_address)
    else:
        byte_img = None

    # getting answer
    answer = str(answer.find('script'))
    left_border_index = answer.find("'") + 1
    right_border_index = answer.rfind("'")
    answer = answer[left_border_index:right_border_index]

    # formatting answer for tasks 19-21, because there are 3 answers
    if 21 >= int(task_number) >= 19:
        answer = answer.replace('1) ', '').replace('<br/>2) ', ';').replace('<br/>3) ', ';')

    # getting excel file
    if '<a' in task_script_text and 'xls' in task_script_text:
        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        excel_address = task_script_text[begin_index:end_index]
        byte_excel = get_excel(excel_address)
    else:
        byte_excel = None

    # getting word file
    if '<a' in task_script_text and 'docx' in task_script_text:
        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        word_address = task_script_text[begin_index:end_index]
        byte_word = get_word(word_address)
    else:
        byte_word = None

    # getting txt file
    if '<a' in task_script_text and 'txt' in task_script_text and task_number != '10':
        if task_number == '27':

            begin_index = task_script_text.rfind('<a') + 9
            end_index = 0
            for i in range(begin_index, len(task_script_text)):
                if task_script_text[i] == '"':
                    end_index = i
                    break
            txg_address_2 = task_script_text[begin_index:end_index]
            byte_txt_2 = get_word(txg_address_2)
        else:
            byte_txt_2 = None

        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        txg_address_1 = task_script_text[begin_index:end_index]
        byte_txt_1 = get_word(txg_address_1)

    else:
        byte_txt_1 = None
        byte_txt_2 = None

    result_task = get_task_text(task_script)
    # add a hint to task 19-21, because there are 3 answers
    if 21 >= int(task_number) >= 19:
        result_task += '\n Ответы на каждый из трех вопросов разделите точкой с запятой(;),' \
                       ' а ответы внутри одного вопроса пробелом'
    return result_task, answer, byte_img, byte_excel, byte_word, byte_txt_1, byte_txt_2


if __name__ == '__main__':
    get_task_by_number('20')
