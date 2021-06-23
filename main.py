import json
import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
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
TASKNUM = 0
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике.'
                              'Выбери номер задания, я выдам тебе задачу. Введи ответ и я проверю его правильность.'
                              'Введите команду /practice, чтобы начать решать задания.'
                              'Чтобы остановить любой диалог нажмите /stop',
                              reply_markup=markup)


def register(update: Update, context: CallbackContext):
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    result = sql_work.register(update.message.from_user.name, update.message.chat_id)
    if not result:
        update.message.reply_text("Вы уже зарегистрированы", reply_markup=markup)
    else:
        update.message.reply_text("Вы успешно зарегистрировались.", reply_markup=markup)


def conv_begin(update: Update, context: CallbackContext):
    update.message.reply_text("Выбирете номер задания от 1 до 27")
    return 1


def help_command(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Привет! Напиши /start, чтобы начать работу', reply_markup=markup)


def practice(update: Update, context: CallbackContext):
    global TASKNUM
    if update.message.text == '/stop':
        reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике. \
Выбери номер задания, я выдам тебе задачу. Введи ответ и я проверю его правильность. \
Введите команду /practice, чтобы начать решать задания. \
Чтобы смотреть теорию, напишите /theory', reply_markup=markup)
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
        TASKNUM = task_number
        task, answer, img_adr, xls_adr, doc_adr = get_task_by_number(task_number)

        global ANSWER
        ANSWER = answer
        print('Answer:', ANSWER)
        update.message.reply_text(task)
        if img_adr:
            bytestring = get_photo(img_adr)
            with open('temp_task_files/task.png', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("temp_task_files/task.png", "rb")
            update.message.reply_photo(file)
        if xls_adr:
            bytestring = get_excel(xls_adr)
            with open('temp_task_files/file.xlsx', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("temp_task_files/file.xlsx", "rb")
            update.message.reply_document(file)
        if doc_adr:
            bytestring = get_word(doc_adr)
            with open('temp_task_files/file.docx', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("temp_task_files/file.docx", "rb")
            update.message.reply_document(file)
        return 2
    except Exception:
        update.message.reply_text('Что-то пошло не так, попробуйте еще раз')
        return 1


def stats(update, context):
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    result = sql_work.get_stats(update.message.chat_id)
    if not result:
        update.message.reply_text("Вы не можете смотреть свою статистику, не зарегистрировавшись", reply_markup=markup)
        return
    for task_number, answers in result.items():
        update.message.reply_text(
            f"На задаче {task_number} у вас {answers[0]} успешных решений из {answers[1]}",
            reply_markup=markup)


def theory(update, context):
    if update.message.text == '/stop':
        reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике. \
        Выбери номер задания, я выдам тебе задачу. Введи ответ и я проверю его правильность. \
        Введите команду /practice, чтобы начать решать задания. \
        Чтобы смотреть теорию, напишите /theory', reply_markup=markup)
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

        reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(f'По этой теме можешь посмотреть видео:\n'
                                  f'{get_theory_video(theory_links[task_number])}\n'
                                  f'Или почитать теорию на сайте:\n'
                                  f'{theory_links[task_number]}')
        update.message.reply_text('Чтобы решать задания введи /practice. Чтобы продолжить читать теорию введи /theory',
                                  reply_markup=markup,
                                  )
        
        return ConversationHandler.END
    except Exception:
        reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Что-то пошло не так, попробуйте еще раз', reply_markup=markup)
        return 1


def check(update: Update, context: CallbackContext):
    global TASKNUM
    if update.message.text == '/stop':
        update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике. \
    Выбери номер задания, я выдам тебе задачу. Введи ответ и я проверю его правильность. \
    Введите команду /practice, чтобы начать решать задания. \
    Чтобы смотреть теорию, напишите /theory')
        return ConversationHandler.END
    global ANSWER
    ANSWER.lstrip().rstrip()

    user_answer = update.message.text
    user_answer.lstrip().rstrip()
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if str(ANSWER) == str(user_answer):
        update.message.reply_text(f'Вы аблолютно правы. Ответ: {user_answer}', reply_markup=markup)
        status = sql_work.add_score(TASKNUM, 1, update.message.chat_id)
    else:
        update.message.reply_text(f'Ваш ответ неверен. Ответ: {ANSWER}. '
                                  f'Чтобы решать дальше напшите /practice',
                                  reply_markup=markup)
        status = sql_work.add_score(TASKNUM, 0, update.message.chat_id)
    if not status:
        update.message.reply_text("Вы еще не зарегистрированы, поэтому это решение не учитывается в статистике.",
                                  reply_markup=markup)
    return ConversationHandler.END


def send_photo(update: Update, context: CallbackContext) -> None:
    bytestring = get_photo("60.gif")
    with open('temp_task_files/task.png', 'wb') as imagefile:
        imagefile.write(bytestring)
    file = open("temp_task_files/task.png", "rb")
    update.message.reply_photo(file)
    update.message.reply_text("(№ 3652) (С.В. Логинова) Логическая функция F задаётся выражением (x ∧ y) ∨ (¬x ∧ ¬z).")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("reg", register))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("send", send_photo))
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

    dispatcher.add_handler(practice_dialog)
    dispatcher.add_handler(theory_dialog)
    dispatcher.add_handler(MessageHandler(Filters.text, help_command))



    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
