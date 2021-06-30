import json
import logging
from pprint import pprint

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, ConversationHandler, InlineQueryHandler, CallbackQueryHandler
from theory_video import get_theory_video

from get_files import get_photo, get_excel, get_word
from task_by_number import get_task_by_number
import sql_work
from config import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
ANSWER = ""
VARIANT = []
TASK_NUMBER = 0
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
                              'Выбери номер задания, я выдам тебе задачу.'
                              ' Введи ответ и я проверю его правильность.'
                              'Введите команду /practice, чтобы начать решать задания.'
                              'Чтобы остановить любой диалог нажмите /stop',
                              reply_markup=markup)
    # register user
    sql_work.register(update.message.from_user.name, update.message.chat_id)


def conv_begin(update: Update, context: CallbackContext):
    update.message.reply_text("Выбирете номер задания от 1 до 27")
    return 1


def help_command(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет! Напиши /start, чтобы начать работу', reply_markup=markup)


def practice(update: Update, context: CallbackContext):
    global TASK_NUMBER
    if update.message.text == '/stop':
        reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
            'Выбери номер задания, я выдам тебе задачу.'
            ' Введи ответ и я проверю его правильность.'
            'Введите команду /practice, чтобы начать решать задания.'
            'Чтобы остановить любой диалог нажмите /stop',
            reply_markup=markup)
        return ConversationHandler.END

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
    task, answer, img_adr, xls_adr, doc_adr = get_task_by_number(task_number)
    global ANSWER
    ANSWER = answer
    print('Answer:', ANSWER)
    update.message.reply_text(task)
    if img_adr:
        update.message.reply_photo(img_adr)
    if xls_adr:
        with open('temp_task_files/file.docx', 'wb') as xlsx:
            xlsx.write(xls_adr)
        file = open("temp_task_files/file.xlsx", "rb")
        update.message.reply_document(file)
    if doc_adr:
        with open('temp_task_files/file.docx', 'wb') as docx:
            docx.write(doc_adr)
        file = open("temp_task_files/file.docx", "rb")
        update.message.reply_document(file)
    return 2
    # except Exception:
    #     update.message.reply_text('Что-то пошло не так, попробуйте еще раз')
    #     return 1



def get_variant():
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    variant = []
    for task_number in range(1, 28):
        if 22 > task_number > 19:
            continue
        task, answer, img_adr, xls_adr, doc_adr = get_task_by_number(str(task_number))

        global ANSWER
        ANSWER = answer
        print('Answer:', ANSWER)
        all_task_materials = []
        all_task_materials.append(task)
        all_task_materials.append(answer)
        if img_adr:
            byte_string = get_photo(img_adr)
            with open('temp_task_files/task.png', 'wb') as image:
                image.write(byte_string)
            file = open("temp_task_files/task.png", "rb")
            all_task_materials.append(file)
        if xls_adr:
            byte_string = get_excel(xls_adr)
            with open('temp_task_files/file.xlsx', 'wb') as xls:
                xls.write(byte_string)
            file = open("temp_task_files/file.xlsx", "rb")
            all_task_materials.append(file)
        if doc_adr:
            byte_string = get_word(doc_adr)
            with open('temp_task_files/file.docx', 'wb') as docx:
                docx.write(byte_string)
            file = open("temp_task_files/file.docx", "rb")
            all_task_materials.append(file)
        variant.append(all_task_materials)
    return variant


def send_variant(update, context):
    global VARIANT
    VARIANT = get_variant()
    keyboard = []
    addl = []
    for i in range(1, 28):
        if 21 <= i <= 22:
            continue
        addl.append(InlineKeyboardButton(f'{i}', callback_data=i))
        if len(addl) == 5:
            keyboard.append(addl)
            addl = []
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ваш вариант:", reply_markup=reply_markup)


def stats(update, context):
    reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    result = sql_work.get_stats(update.message.chat_id)
    if not result:
        update.message.reply_text("Вы пока не решали задачи. Если хотите попробовать: /practice",
                                  reply_markup=markup)
        return
    for task_number, answers in result.items():
        correctness = int(answers[0] / answers[1] * 100)
        if correctness > 90:
            reply = 'Отличный результат. Продолжай в том же духе.'
        elif correctness > 75:
            reply = 'Хороший результат. У тебя все получиться!'
        elif correctness > 50:
            reply = 'Есть, над чем работать, но в целом неплохо'
        else:
            reply = 'Рекомендую тебе почитать теорию по этой задаче'

        update.message.reply_text(
            f"На задаче {task_number} у вас {answers[0]} успешных решений из {answers[1]}"
            f" Правильность: {correctness}%\n"
            f"{reply}",
            reply_markup=markup)


def theory(update, context):
    if update.message.text == '/stop':
        reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
            'Выбери номер задания, я выдам тебе задачу.'
            ' Введи ответ и я проверю его правильность.'
            'Введите команду /practice, чтобы начать решать задания.'
            'Чтобы остановить любой диалог нажмите /stop',
            reply_markup=markup)
        return ConversationHandler.END
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

        reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
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
        reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Что-то пошло не так, попробуйте еще раз', reply_markup=markup)
        return 1


def check(update: Update, context: CallbackContext):
    global TASK_NUMBER
    if update.message.text == '/stop':
        reply_keyboard = [['/practice', '/theory'], ['/stats', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
            'Выбери номер задания, я выдам тебе задачу.'
            ' Введи ответ и я проверю его правильность.'
            'Введите команду /practice, чтобы начать решать задания.'
            'Чтобы остановить любой диалог нажмите /stop',
            reply_markup=markup)
        return ConversationHandler.END
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
            1: [MessageHandler(Filters.text, start)]
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(full_var_dialog)
    dispatcher.add_handler(practice_dialog)
    dispatcher.add_handler(theory_dialog)
    dispatcher.add_handler(MessageHandler(Filters.text, help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
