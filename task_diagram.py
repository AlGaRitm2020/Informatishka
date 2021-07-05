"""
=========
Pie Demo2
=========
Make a pie charts using `~.axes.Axes.pie`.
This example demonstrates some pie chart features like labels, varying size,
autolabeling the percentage, offsetting a slice and adding a shadow.
"""

import matplotlib.pyplot as plt
import os


def get_task_stats_diagram(task_number, right_answers, all_answers, result):
    wrong_answers = all_answers - right_answers
    labels = [f'Верный ответ: {right_answers}', f'Неверный ответ: {wrong_answers}']
    values = [right_answers, wrong_answers]

    # Make figure and axes
    fig, ax = plt.subplots(1, 1)
    ax.set_title(f"Статистика по задаче {task_number}", fontsize=20)
    ax.set_xlabel(result, fontsize=12)

    # A standard pie plot
    patches, texts, autotexts = ax.pie(values,
                                       autopct='%.0f%%',
                                       textprops={'size': 'larger'},
                                       shadow=False, radius=0.9,
                                       explode=(0, 0.05))

    ax.legend(labels, loc='upper left', bbox_to_anchor=(0.7, 0.9))
    plt.setp(autotexts, size='x-large')

    # getting bytes from image
    plt.savefig('task_stats.png')
    with open('task_stats.png', mode='rb') as img:
        byte_img = img.read()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'task_stats.png')
    os.remove(path)
    plt.close()

    return byte_img


if __name__ == '__main__':
    print(get_task_stats_diagram(1, 1, 1))
