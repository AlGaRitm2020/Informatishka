import html


def get_all_tasks(task):
    task = str(task)
    result = ""
    text_begin = task.find("(")
    text_end = task.find(")")
    shit_end = task.find(";")
    result += task[text_begin + 4] + html.unescape(task[text_begin + 5:shit_end]) + task[shit_end + 1:text_end]
    text_begin = task.find("changeImageFilePath") + len("changeImageFilePath") + 2
    text_end = task.rfind("'")
    word_changed = ""
    for i in range(text_begin, text_end):
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

