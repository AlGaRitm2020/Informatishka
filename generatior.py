from pprint import pprint

from bs4 import BeautifulSoup
import requests
import random

from get_files import get_excel, get_photo, get_word
from task_text_parser import get_task_text


def generate_random_variant():
    VAR_ID = random.randint(1, 5000)
    VAR_ID = 20
    URL = f'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&answers=on&varId={VAR_ID}'
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    center = soup.find('div', class_='center')
    tasks_table = center.find('table', class_='vartopic')

    tasks_td = tasks_table.findAll('td', class_='topicview')
    tasks_script = [i.find('script') for i in tasks_td]

    answer_table = center.find('table', class_='varanswer')
    answer_td_list = answer_table.findAll('td', class_='answer')
    answers = []
    for i, elem in enumerate(answer_td_list):
        if i + 1 == 20:
            answers.append(None)
            answers.append(None)
        if elem.text:
            answers.append(elem.text)
        else:
            answers.append(str(elem).split("'")[1].replace('<br/>', '\n'))

    byte_img_list = []
    byte_excel_list = []
    byte_word_list = []
    byte_txt_list = []
    for task_number in range(len(tasks_script)):
        """
           making bytes objects lists
        """
        task_script_text = str(tasks_script[task_number])
        # --- making img byte list
        if 'img' in task_script_text:
            begin_index = task_script_text.find('img') + 9
            end_index = 0
            for i in range(begin_index, len(task_script_text)):
                if task_script_text[i] == '"':
                    end_index = i
                    break
            img_address = task_script_text[begin_index:end_index]
            byte_img_list.append(get_photo(img_address))
            byte_excel_list.append(None)
            byte_word_list.append(None)
            byte_txt_list.append(None)
        # --- making txt bytes list ---
        elif '<a' in task_script_text and 'txt' in task_script_text and task_number != 10 - 1:
            # task_number == 27
            if task_number == 27 - 3:
                begin_index_1, begin_index_2 = task_script_text.find('<a') + 9, \
                                               task_script_text.rfind('<a') + 9
                end_index_1, end_index_2 = 0, 0
                for i in range(begin_index_1, len(task_script_text)):
                    if task_script_text[i] == '"':
                        end_index_1 = i
                        break
                for i in range(begin_index_2, len(task_script_text)):
                    if task_script_text[i] == '"':
                        end_index_2 = i
                        break
                txg_address_1 = task_script_text[begin_index_1:end_index_1]
                txg_address_2 = task_script_text[begin_index_2:end_index_2]
                byte_txt_list.append((get_word(txg_address_1), get_word(txg_address_2)))
            else:
                begin_index = task_script_text.find('<a') + 9
                end_index = 0
                for i in range(begin_index, len(task_script_text)):
                    if task_script_text[i] == '"':
                        end_index = i
                        break
                txg_address_1 = task_script_text[begin_index:end_index]
                byte_txt_list.append(get_word(txg_address_1))

            byte_img_list.append(None)
            byte_word_list.append(None)
            byte_excel_list.append(None)
        # --- making xls and docx bytes lists ---
        elif '<a' in task_script_text and 'xls' or 'docx' in task_script_text:
            begin_index = task_script_text.find('<a') + 9
            end_index = 0
            for i in range(begin_index, len(task_script_text)):
                if task_script_text[i] == '"':
                    end_index = i
                    break
            address = task_script_text[begin_index:end_index]
            if 'xls' in task_script_text:
                byte_excel_list.append(get_excel(address))
                byte_word_list.append(None)
            else:
                byte_word_list.append(get_word(address))
                byte_excel_list.append(None)

            byte_img_list.append(None)
            byte_txt_list.append(None)

        else:
            byte_img_list.append(None)
            byte_txt_list.append(None)
            byte_word_list.append(None)
            byte_excel_list.append(None)

    tasks_description = []
    for task_number in range(len(tasks_script)):
        tasks_description.append(get_task_text(tasks_script[task_number]))
        # add a hint to task 19-21, because there are 3 answers
        if task_number - 1 == 19:
            tasks_description[task_number] += '\n Ответы на каждый из трех вопросов вводите в новой' \
                                              ' строке точкой с запятой(;), а ответы внутри одного' \
                                              ' вопроса пробелом'

    variant = []
    task_number = 1
    for task_description, answer, byte_img, byte_excel, byte_word, byte_txt in zip(tasks_description,
                                                                                   answers,
                                                                                   byte_img_list,
                                                                                   byte_excel_list,
                                                                                   byte_word_list,
                                                                                   byte_txt_list):
        if task_number == 20:
            task_number = 22
            variant.append(None)
            variant.append(None)
        if isinstance(byte_txt, tuple):
            byte_txt_1 = byte_txt[0]
            byte_txt_2 = byte_txt[1]
        else:
            byte_txt_1 = byte_txt
            byte_txt_2 = None

        task = [task_description, answer]

        if byte_img:
            task.append(byte_img)
        if byte_excel:
            with open(f'temp_task_files/{task_number}.xlsx', 'wb') as xls:
                xls.write(byte_excel)
            file = open(f"temp_task_files/{task_number}.xlsx", "rb")
            task.append(file)
        if byte_word:
            with open(f'temp_task_files/{task_number}.docx', 'wb') as docx:
                docx.write(byte_word)
            file = open(f"temp_task_files/{task_number}.docx", "rb")
            task.append(file)
        if byte_txt_1:
            with open(f"temp_task_files/{task_number}_A.txt", 'wb') as docx:
                docx.write(byte_txt_1)
            file = open(f"temp_task_files/{task_number}_A.txt", "rb")
            task.append(file)
        if byte_txt_2:
            with open(f"temp_task_files/{task_number}_B.txt", 'wb') as docx:
                docx.write(byte_txt_2)
            file = open(f"temp_task_files/{task_number}_B.txt", "rb")
            task.append(file)

        variant.append(task)
        task_number += 1

    return variant


if __name__ == '__main__':
    print(generate_random_variant()[9])
