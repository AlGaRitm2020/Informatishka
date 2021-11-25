import matplotlib.pyplot as plt
import os


async def get_task_stats_diagram(task_number, right_answers, all_answers, result):
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
                                       shadow=False, radius=0.95,
                                       explode=(0, 0.05))

    ax.legend(labels, loc='upper left', bbox_to_anchor=(0.7, 0.8))
    plt.setp(autotexts, size='x-large')

    # getting bytes from image
    plt.savefig('data/temp_task_files/task_stats.png')
    byte_img = open('data/temp_task_files/task_stats.png', mode='rb').read()
    plt.close()

    return byte_img
