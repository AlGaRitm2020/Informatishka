from task_text_parser import get_task_text
from pprint import pprint

with open('src/for_test_task_parser.txt', encoding='utf-8') as task:
    pprint(get_task_text(task.read()))