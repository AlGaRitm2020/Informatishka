import html
from pprint import pprint


def get_task_text(task):
    task = str(task)
    pprint(task)
    result_task = ""
    begin_num_index = task.find("(")
    end_num_index = task.find(")")
    end_line_index = task.find(";")
    result_task += task[begin_num_index + 4] + html.unescape(task[begin_num_index + 5:end_line_index]) + task[end_line_index + 1:end_num_index]
    begin_num_index = task.find("changeImageFilePath") + len("changeImageFilePath") + 2
    end_num_index = task.rfind("'")
    word_changed = ""
    for i in range(begin_num_index, end_num_index):
        if not word_changed:
            if task[i] == '&':
                word_changed += task[i]
            else:
                result_task += task[i]
        else:
            if task[i] == ';':
                word_changed += task[i]
                result_task += html.unescape(word_changed)
                word_changed = ""
            else:
                word_changed += task[i]

    in_tag = False
    html_tag = ''
    cleaned_task = result_task

    for i in range(len(result_task)):
        if result_task[i] == '<' and result_task[i + 1] != ' ':
            in_tag = True
        if in_tag:
            html_tag += result_task[i]
        if result_task[i] == '>' and result_task[i - 1] != ' ':
            in_tag = False
            if html_tag == '<br/>':
                cleaned_task = cleaned_task.replace(html_tag, '\n')
                html_tag = ''
            elif html_tag == "<sup>":
                cleaned_task = cleaned_task.replace(html_tag, '"')
                html_tag = ''
            else:
                cleaned_task = cleaned_task.replace(html_tag, '')
                html_tag = ''

    result_task = cleaned_task

    # replace 'ПаскальPythonС++' string
    result_task = result_task.replace('PythonС++', '\n ').replace('PythonСи', '\n')

    # add languages names for codes
    result_task = result_task.replace('Паскаль', '\nПаскаль:')
    result_task = result_task.replace('end.\n', 'end.\n\nPython:\n')
    result_task = result_task.replace('#include', '\nC/C++:\n#include')
    return result_task
