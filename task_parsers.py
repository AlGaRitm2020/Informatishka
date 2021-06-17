import html
from pprint import pprint


def get_all_tasks(task):
    task = str(task)
    # pprint(task)
    result = ""
    begin_num_index = task.find("(")
    end_num_index = task.find(")")
    end_line_index = task.find(";")
    result += task[begin_num_index + 4] + html.unescape(task[begin_num_index + 5:end_line_index]) + task[end_line_index + 1:end_num_index]
    begin_num_index = task.find("changeImageFilePath") + len("changeImageFilePath") + 2
    end_num_index = task.rfind("'")
    word_changed = ""
    for i in range(begin_num_index, end_num_index):
        if not word_changed:
            if task[i] == '&':
                word_changed += task[i]
            else:
                result += task[i]
        else:
            if task[i] == ';':
                word_changed += task[i]
                result += html.unescape(word_changed)
                word_changed = ""
            else:
                word_changed += task[i]
    return result
