from pprint import pprint
from bs4 import BeautifulSoup
import requests
import random
from task_text_parser import get_task_text


def get_task_by_number(task_number):
    categories_dict = {
        '1': 'cat12=on&cat13=on',
        '2': 'cat8=on',
        '3': 'cat16=on',
        '4': 'cat21=on&cat22=on&cat23=on&cat25=on',
        '5': 'cat27=on&cat28=on&cat144=on',
        '6': 'cat37=on&cat91=on',
        '7': 'cat38=on&cat39=on',
        '8': 'cat42=on&cat43=on&cat145=on',
        '9': 'cat146=on&cat147=on',
        '10': 'cat148=on',
        '11': 'cat52=on&cat53=on&cat54=on&cat149=on',
        '12': 'cat55=on&cat56=on&cat57=on&cat58=on',
        '13': 'cat59=on',
        '14': 'cat60=on&cat61=on&cat62=on',
        '15': 'cat67=on&cat68=on&cat69=on&cat70=on&cat123=on',
        '16': 'cat44=on&cat45=on&cat46=on',
        '17': 'cat150=on&cat151=on',
        '18': 'cat152=on&cat153=on&cat165=on',
        '19': 'cat154=on&cat163=on',
        '20': 'cat154=on&cat163=on',
        '21': 'cat154=on&cat163=on',
        '22': 'cat73=on&cat74=on',
        '23': 'cat78=on&cat79=on&cat80=on&cat162=on',
        '24': 'cat155=on&cat156=on&cat164=on',
        '25': 'cat157=on&cat158=on&cat159=on',
        '26': 'cat160=on',
        '27': 'cat161=on',
    }
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
        ind = task_script_text.find('img') + 9
        ind1 = 0
        for j in range(ind, len(task_script_text)):
            if task_script_text[j] == '"':
                ind1 = j
                break
        img_address = task_script_text[ind:ind1]
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
        ind = task_script_text.find('<a') + 9
        ind1 = 0
        for j in range(ind, len(task_script_text)):
            if task_script_text[j] == '"':
                ind1 = j
                break
        excel_address = task_script_text[ind:ind1]
    else:
        excel_address = None

    # making word_files list
    if '<a' in task_script_text and 'docx' in task_script_text:
        ind = task_script_text.find('<a') + 9
        ind1 = 0
        for j in range(ind, len(task_script_text)):
            if task_script_text[j] == '"':
                ind1 = j
                break
        word_address = task_script_text[ind:ind1]
    else:
        word_address = None

    result_task = get_task_text(task_script)

    return result_task, answer, img_address, excel_address, word_address


get_task_by_number('6')
