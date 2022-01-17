import matplotlib.pyplot as plt
import os

def convert_time(sec):
    return sec//60 ,sec%60
async def get_time_stats_diagram(task_number, min_time, max_time, avg_time, recomend_time):

    # Make figure and axes
    fig, ax = plt.subplots(1, 1)
    basic_params = {"fontweight":650}
    header_params = {"color" : "#42b8f6","fontweight":900}
    time_params = {"color": "#ffffff", "fontweight": 900,"fontsize": 15}
    ax.set_title(f"Статистика по задаче {task_number}", fontsize=20,**header_params)

    ax.text(-0.1, 0.9, f"Минимальное время", fontsize=15,**basic_params, color="#0288cc")
    ax.text(0.56, 0.9, f" {convert_time(min_time)[0]}мин {convert_time(min_time)[1]}сек", **time_params)

    ax.text(-0.1, 0.7, f"Максимальное время", fontsize=15,**basic_params, color="#836fed")
    ax.text(0.56, 0.7, f" {convert_time(max_time)[0]}мин {convert_time(max_time)[1]}сек", **time_params)

    ax.text(-0.1, 0.5, f"Среднее время ", fontsize=15,**basic_params, color="#6669ba")
    ax.text(0.56, 0.5, f" {convert_time(avg_time)[0]}мин {convert_time(avg_time)[1]}сек", **time_params)

    ax.text(-0.1, 0.25, f"Рекомендуемое время", fontsize=15,**basic_params, color="#b865fa")
    ax.text(0.56, 0.25, f" {convert_time(recomend_time)[0]}мин {convert_time(recomend_time)[1]}сек", **time_params)

    if recomend_time < avg_time:
        ax.text(0, 0.02, f"Есть, над чем работать, но в целом неплохо.", fontsize=12,**basic_params, color="#cc61ff")
    if recomend_time >= avg_time:
        ax.text(0, 0.02, f"Отличный результат. Продолжай в том же духе.", fontsize=12,**basic_params, color="#cc61ff")


    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_axis_off()

    #ax.set_xlabel(result, fontsize=12)
#
    ## A standard pie plot
    #patches, texts, autotexts = ax.pie(values,
    #                                   autopct='%.0f%%',
    #                                   textprops={'size': 'larger'},
    #                                   shadow=False, radius=0.95,
    #                                   explode=(0, 0.05))
#
    #ax.legend(labels, loc='upper left', bbox_to_anchor=(0.7, 0.8))
    #plt.setp(autotexts, size='x-large')

    # getting bytes from image
    plt.savefig('data/temp_task_files/task_stats.png', facecolor="black")
    byte_img = open('data/temp_task_files/task_stats.png', mode='rb').read()
    plt.close()

    return byte_img
