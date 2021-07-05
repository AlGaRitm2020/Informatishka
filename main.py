import json
import logging
from time import time
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, ConversationHandler, InlineQueryHandler, CallbackQueryHandler

from generatior import generate_random_variant
from task_diagram import get_task_stats_diagram
from theory_video import get_theory_video

from get_files import get_photo, get_excel, get_word
from task_by_number import get_task_by_number

import sql_work

# import token
try:
    # manual start
    # from local config file
    from config import TEST_TOKEN

    TOKEN = TEST_TOKEN
except ModuleNotFoundError:
    # else deployed on Heroku
    # DEPLOY TOKEN - env var on Heroku
    from load_env_vars import DEPLOY_TOKEN

    TOKEN = DEPLOY_TOKEN
    if not TOKEN:
        print('Copy config.py to root directory from Telegram chat')

bot = Bot(TOKEN)
CHAT_ID = ""
MESSAGE_IDS = []
CURRENT_TASK = -1
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
ANSWER = ""
VARIANT = []
ANSWERS = [None] * 27
TASK_NUMBER = 0
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    reply_keyboard = [['/practice', '/theory', '/full'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
                              'Выбери номер задания, я выдам тебе задачу.'
                              ' Введи ответ и я проверю его правильность.'
                              'Введите команду /practice, чтобы начать решать задания.'
                              'Введите команду /theory, чтобы начать смотреть теорию по заданиям.'
                              'Введите команду /full, чтобы начать решать полный вариант.'
                              'Чтобы остановить любой диалог нажмите /stop',
                              reply_markup=markup)
    # register user
    sql_work.register(update.message.from_user.name, update.message.chat_id)
    return ConversationHandler.END


def conv_begin(update: Update, context: CallbackContext):
    update.message.reply_text("Выбирете номер задания от 1 до 27")
    return 1


def help_command(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет! Напиши /start, чтобы начать работу', reply_markup=markup)


def practice(update: Update, context: CallbackContext):
    global TASK_NUMBER
    task_number = update.message.text
    try:
        if int(task_number) < 1 or int(task_number) > 27:
            update.message.reply_text("Номер задания от 1 до 27, попробуй еще раз")
            return 1
    except ValueError:
        "if task_number isn't int"
        update.message.reply_text("Номер задания - целое число от 1 до 27, попробуй еще раз")
        return 1
    TASK_NUMBER = task_number
    task, answer, img_bytes, xls_bytes, doc_bytes, txt_bytes_1, txt_bytes_2 = get_task_by_number(task_number)
    global ANSWER
    ANSWER = answer
    update.message.reply_text(task)
    if img_bytes:
        with open('temp_task_files/task.png', 'wb') as img:
            img.write(img_bytes)
        file = open("temp_task_files/task.png", "rb")
        update.message.reply_document(file)
    if xls_bytes:
        with open('temp_task_files/file.docx', 'wb') as xlsx:
            xlsx.write(xls_bytes)
        file = open("temp_task_files/file.xlsx", "rb")
        update.message.reply_document(file)
    if doc_bytes:
        with open('temp_task_files/file.docx', 'wb') as docx:
            docx.write(doc_bytes)
        file = open("temp_task_files/file.docx", "rb")
        update.message.reply_document(file)
    if txt_bytes_1:
        with open('temp_task_files/A.txt', 'wb') as txt:
            txt.write(txt_bytes_1)
        file = open("temp_task_files/A.txt", "rb")
        update.message.reply_document(file)
    if txt_bytes_2:
        with open('temp_task_files/B.txt', 'wb') as txt:
            txt.write(txt_bytes_2)
        file = open("temp_task_files/B.txt", "rb")
        update.message.reply_document(file)

    return 2
    # except Exception:
    #     update.message.reply_text('Что-то пошло не так, попробуйте еще раз')
    #     return 1


def create_buttons():
    keyboard = []
    addl = []
    for i in range(1, 28):
        if 19 < i < 22:
            continue
        addl.append(InlineKeyboardButton(f'{i}', callback_data=i))
        if len(addl) == 5:
            keyboard.append(addl)
            addl = []
    return InlineKeyboardMarkup(keyboard)


def buttonsHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = create_buttons()
    task_number = int(query.data) - 1
    global VARIANT
    global CHAT_ID
    global MESSAGE_IDS
    global CURRENT_TASK
    if CURRENT_TASK == task_number:
        return
    if not VARIANT:
        return
    task = VARIANT[task_number]
    img_bytes = task['image']
    excel_bytes = task['excel']
    word_bytes = task['word']
    txt_bytes_1 = task['txt1']
    txt_bytes_2 = task['txt2']
    if not CHAT_ID:
        return
    CURRENT_TASK = task_number
    for message_id in MESSAGE_IDS:
        if message_id:
            bot.delete_message(CHAT_ID, message_id)
    MESSAGE_IDS = []
    query.edit_message_text(task['description'], reply_markup=reply_markup)
    if img_bytes:
        MESSAGE_IDS.append(bot.send_photo(CHAT_ID, img_bytes).message_id)
    if excel_bytes:
        file = open(f'temp_task_files/{task_number + 1}.xlsx', 'rb')
        MESSAGE_IDS.append(bot.send_document(CHAT_ID, file).message_id)
    if word_bytes:
        file = open(f'temp_task_files/{task_number + 1}.docx', 'rb')
        MESSAGE_IDS.append(bot.send_document(CHAT_ID, file).message_id)
    if txt_bytes_1:
        file = open(f'temp_task_files/{task_number + 1}_A.txt', 'rb')
        MESSAGE_IDS.append(bot.send_document(CHAT_ID, file).message_id)
    if txt_bytes_2:
        file = open(f'temp_task_files/{task_number + 1}_B.txt', 'rb')
        MESSAGE_IDS.append(bot.send_document(CHAT_ID, file).message_id)


def answerWrighter(update: Update, context: CallbackContext):
    answer = update.message.text
    if answer[:5] == '/stop':
        fullVarChecker(update, context)
        return ConversationHandler.END
    reply_markup = create_buttons()
    global ANSWERS
    global CURRENT_TASK
    if CURRENT_TASK == -1:
        update.message.reply_text("Сначала выберите задание", reply_markup=reply_markup)
        return 1
    ANSWERS[CURRENT_TASK] = answer
    update.message.reply_text("Ваш ответ записан", reply_markup=reply_markup)
    return 1


def fullVarChecker(update: Update, context: CallbackContext):
    import sql_work
    global ANSWERS
    global VARIANT
    solved = 0
    all = 0
    for number in range(27):
        if not VARIANT[number]:
            continue
        user_answer = ANSWERS[number]
        if not user_answer:
            continue
        all += 1
        correct_answer = VARIANT[number]['answer']
        update.message.reply_text(f'Ваш ответ на задачу {str(number + 1)}: {str(user_answer)} ; Правильный ответ: {str(correct_answer)}')
        user_answer = user_answer.lower()
        correct_answer = correct_answer.lower()
        user_answer = user_answer.replace('\n', ';')
        correct_answer = correct_answer.replace('\n', ';')
        user_answer = user_answer.replace(' ', '')
        correct_answer = correct_answer.replace(' ', '')
        if user_answer == correct_answer:
            solved += 1
        else:
            print(user_answer)
            print(correct_answer)
        sql_work.add_score(number + 1, int(user_answer == correct_answer), update.message.chat_id)
    update.message.reply_text(f'В этом варианте у вас решено правильно {str(solved)} задач из {str(all)}')
    ANSWERS = [None] * 27


def send_variant(update, context):
    global VARIANT
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    VARIANT = generate_random_variant()
    reply_markup = create_buttons()
    update.message.reply_text("Чтобы закончить решать и посмотреть результаты по этмоу варианту напишите /stop"
                              "Ваш вариант:", reply_markup=reply_markup)
    return 1


def stats(update, context):
    reply_keyboard = [['/practice', '/theory', '/full'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    result = sql_work.get_stats(update.message.chat_id)
    if not result:
        update.message.reply_text("Вы пока не решали задачи. Если хотите попробовать: /practice",
                                  reply_markup=markup)

        return
    for task_number, answers in result.items():
        correctness = int(answers[0] / answers[1] * 100)
        if correctness > 90:
            result = 'Отличный результат. Продолжай в том же духе.'
        elif correctness > 75:
            result = 'Хороший результат. У тебя все получиться!'
        elif correctness > 50:
            result = 'Есть, над чем работать, но в целом неплохо'
        else:
            result = 'Рекомендую тебе почитать теорию по этой задаче'

        stat_diagram = get_task_stats_diagram(task_number, answers[0], answers[1], result)
        update.message.reply_photo(stat_diagram, reply_markup=markup)


def theory(update, context):
    try:
        task_number = update.message.text
        try:
            if int(task_number) < 1 or int(task_number) > 27:
                update.message.reply_text("Номер задания от 1 до 27, попробуй еще раз")
                return 1
        except ValueError:
            "if task_number isn't int"
            update.message.reply_text("Номер задания - целое число от 1 до 27, попробуй еще раз")
            return 1
        with open('data/theory_links.json', 'r') as file:
            theory_links = json.load(file)
        reply_keyboard = [['/practice', '/theory', '/full'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(f'По этой теме можешь посмотреть видео:\n'
                                  f'{get_theory_video(theory_links[task_number])}\n'
                                  f'Или почитать теорию на сайте:\n'
                                  f'{theory_links[task_number]}')
        update.message.reply_text('Чтобы решать задания введи /practice.'
                                  ' Чтобы продолжить читать теорию введи /theory',
                                  reply_markup=markup)
        return ConversationHandler.END
    except Exception:
        reply_keyboard = [['/practice', '/theory', '/full'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Что-то пошло не так, попробуйте еще раз', reply_markup=markup)
        return 1


def check(update: Update, context: CallbackContext):
    global TASK_NUMBER
    global ANSWER
    ANSWER.lstrip().rstrip()
    user_answer = update.message.text
    user_answer.lstrip().rstrip()
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if str(ANSWER) == str(user_answer):
        update.message.reply_text(f'Вы аблолютно правы. Ответ: {user_answer}', reply_markup=markup)
        status = sql_work.add_score(TASK_NUMBER, 1, update.message.chat_id)
    else:
        update.message.reply_text(f'Ваш ответ неверен. Ответ: {ANSWER}. '
                                  f'Чтобы решать дальше напшите /practice',
                                  reply_markup=markup)
        status = sql_work.add_score(TASK_NUMBER, 0, update.message.chat_id)
    if not status:
        update.message.reply_text("Вы еще не зарегистрированы, поэтому это решение не учитывается "
                                  "в статистике.",
                                  reply_markup=markup)
    return ConversationHandler.END


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    practice_dialog = ConversationHandler(
        entry_points=[CommandHandler('practice', conv_begin)],
        states={
            1: [MessageHandler(Filters.text, practice)],
            2: [MessageHandler(Filters.text, check)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )
    theory_dialog = ConversationHandler(
        entry_points=[CommandHandler('theory', conv_begin)],
        states={
            1: [MessageHandler(Filters.text, theory)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )
    full_var_dialog = ConversationHandler(
        entry_points=[CommandHandler('full', send_variant)],
        states={
            1: [MessageHandler(Filters.text, answerWrighter)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )
    dispatcher.add_handler(CommandHandler("stop", start))
    dispatcher.add_handler(CallbackQueryHandler(buttonsHandler))
    dispatcher.add_handler(full_var_dialog)
    dispatcher.add_handler(practice_dialog)
    dispatcher.add_handler(theory_dialog)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(MessageHandler(Filters.text, help_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
