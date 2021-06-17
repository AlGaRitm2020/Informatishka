import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import get_files
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
    update.message.reply_text('Привет, я бот Информатишка. Я помогу тебе в сдаче ЕГЭ по информатике. \
Выбери номер задания, я выдам тебе задачу. Введи ответ и я проверю его правильность. \
Введите команду /practice, чтобы начать решать задания. \
Чтобы смотреть теорию, напишите /theory', reply_markup=markup)


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
        nom = update.message.text
        if int(nom) < 1 or int(nom) > 27:
            update.message.reply_text("Номер задания от 1 до 27, попробуй еще раз")
            return 1
        TASKNUM = nom
        info = get_task_by_number(nom)
        answer = info[1]
        task = info[0]
        img_adr = info[2]
        xls_adr = info[3]
        doc_adr = info[4]
        global ANSWER
        ANSWER = answer[0]
        print(ANSWER)
        update.message.reply_text(task)
        if img_adr:
            import get_files
            bytestring = get_files.get_photo(img_adr)
            with open('imgs/task.png', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("imgs/task.png", "rb")
            update.message.reply_photo(file)
        if xls_adr:
            import get_files
            bytestring = get_files.get_excel(xls_adr)
            with open('imgs/file.xlsx', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("imgs/file.xlsx", "rb")
            update.message.reply_document(file)
        if doc_adr:
            import get_files
            bytestring = get_files.get_word(doc_adr)
            with open('imgs/file.docx', 'wb') as imagefile:
                imagefile.write(bytestring)
            file = open("imgs/file.docx", "rb")
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
    for item in result:
        update.message.reply_text(
            "На задаче {} у вас {} успешных решений за последнюю неделю.".format(item, result[item]), reply_markup=markup)


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
        themes_list = ['https://code-enjoy.ru/ege_po_informatike_2021_zadanie_1_osobie_tochki/',
                       'https://code-enjoy.ru/ege_po_informatike_zadanie_2_moshneyshiy_metod/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_3_baza_dannih/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_4_uslovie_fano/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_5_algoritmi_avtomati/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_6_cikli/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_7_foto_zvuk/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_8_super_razbor/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_9_tablica_excel/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_10_tekstoviy_redaktor/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_11_kolichestvo_informacii/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_12_ukrosheniye_robota/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_13_legkoe/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_14_chempionskaya_podgotoka/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_15_prostim_yazikom/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_16_rekursiya/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_17_pishem_programmu/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_18_tablica_chisel/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_19_igraem_i_viigrivaem/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_20_ubileyniy_vipusk/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_21_igroki_v_igre/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_22_analiziruem_programmu/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_23_opiraemsa_na_predidushie_shagi/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_24_obrabotka_simvolnoy_informacii/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_25_obrabotka_celochislennoy_informacii/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_26_sortirovka/',
                       'https://code-enjoy.ru/ege_po_informatike_2021_zadanie_27_zakluchitelnoye/']
        id = int(update.message.text)
        reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('По этой теме можешь почитать теорию по ссылке:\
{}'.format(themes_list[id - 1]))
        update.message.reply_text('Чтобы решать задания введи /practice. Чтобы продолжить читать теорию введи /theory',
                                  reply_markup=markup)
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
    ANSWER.lstrip()
    ANSWER.rstrip()
    user_answer = update.message.text
    user_answer.lstrip()
    user_answer.rstrip()
    reply_keyboard = [['/practice', '/theory'], ['/reg', '/stats']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if str(ANSWER) == str(user_answer):
        update.message.reply_text('Вы аблолютно правы. Ответ: {}'.format(user_answer), reply_markup=markup)
        status = sql_work.add_score(TASKNUM, 1, update.message.chat_id)
        if not status:
            update.message.reply_text("Вы еще не зарегистрированы, поэтому эт решение не учитывается в статистике.",
                                      reply_markup=markup)
        return ConversationHandler.END
    else:
        update.message.reply_text('Ваш ответ неверен. Ответ: {}. \
Чтобы решать дальше напшите /practice'.format(ANSWER), reply_markup=markup)
        status = sql_work.add_score(TASKNUM, 0, update.message.chat_id)
        if not status:
            update.message.reply_text("Вы еще не зарегистрированы, поэтому эт решение не учитывается в статистике.",
                                      reply_markup=markup)
        return ConversationHandler.END


def send_photo(update: Update, context: CallbackContext) -> None:
    bytestring = get_files.get_photo("60.gif")
    with open('imgs/task.png', 'wb') as imagefile:
        imagefile.write(bytestring)
    file = open("imgs/task.png", "rb")
    update.message.reply_photo(file)
    update.message.reply_text("(№ 3652) (С.В. Логинова) Логическая функция F задаётся выражением (x ∧ y) ∨ (¬x ∧ ¬z).")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("reg", register))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("send", send_photo))
    dispatcher.add_handler(CommandHandler("start", start))
    Dialog = ConversationHandler(
        entry_points=[CommandHandler('practice', conv_begin)],
        states={
            1: [MessageHandler(Filters.text, practice)],
            2: [MessageHandler(Filters.text, check)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )

    Dialog_theory = ConversationHandler(
        entry_points=[CommandHandler('theory', conv_begin)],
        states={
            1: [MessageHandler(Filters.text, theory)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )
    # dispatcher.add_handler(CommandHandler("photo", send_photo))
    dispatcher.add_handler(Dialog)
    dispatcher.add_handler(Dialog_theory)
    dispatcher.add_handler(MessageHandler(Filters.text, help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
