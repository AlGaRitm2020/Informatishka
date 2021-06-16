from task_parsers import get_all_tasks
from pprint import pprint

with open('src/for_test_task_parser.txt', encoding='utf-8') as task:
    pprint(get_all_tasks(task.read()))