from bs4 import BeautifulSoup
import requests
import random

import json
from . import get_files
from .task_text_parser import get_task_text
import asyncio


async def get_task_by_id(task_id):

    url = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewTopic&topicId=' \
          f'{task_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    task_td = soup.find('td', class_='topicview')
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
        byte_img = get_files.get_photo(img_address)
    else:
        byte_img = None

    # getting answer
    answer = str(task_script.find('script'))
    left_border_index = answer.find("'") + 1
    right_border_index = answer.rfind("'")
    answer = answer[left_border_index:right_border_index]
    answer = str(soup.find('div', class_='hidedata').text)
    # formatting answer for tasks 19-21, because there are 3 answers

    # getting excel file
    if '<a' in task_script_text and 'xls' in task_script_text:
        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        excel_address = task_script_text[begin_index:end_index]
        byte_excel = get_files.get_excel(excel_address)
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
        byte_word = get_files.get_word(word_address)
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
            byte_txt_2 = get_files.get_word(txg_address_2)
        else:
            byte_txt_2 = None

        begin_index = task_script_text.find('<a') + 9
        end_index = 0
        for i in range(begin_index, len(task_script_text)):
            if task_script_text[i] == '"':
                end_index = i
                break
        txg_address_1 = task_script_text[begin_index:end_index]
        byte_txt_1 = get_files.get_word(txg_address_1)

    else:
        byte_txt_1 = None
        byte_txt_2 = None

    result_task = asyncio.create_task(get_task_text(task_script))
    await asyncio.gather(result_task)
    return result_task.result(), answer, byte_img, byte_excel, byte_word, byte_txt_1, byte_txt_2


if __name__ == '__main__':
    print(asyncio.run(get_task_by_number('1')))
