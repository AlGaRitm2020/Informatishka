import telebot
from config import TOKEN
from sql_work import get_all_users_chat_ids
TOKEN = "1764376133:AAFg2ygNpY_4I8G4WhvKplcJEKX0RCiHcKY"


def get_announcement_from_markdown(file):
    with open(file, mode='r', encoding='utf-8') as md:
        announcement = md.read().replace('<br>', '')
    return announcement
print(get_announcement_from_markdown('data/announcements/1_migration.md'))

bot = telebot.TeleBot(TOKEN)
chat_ids = [i[0] for i in get_all_users_chat_ids()]
print(chat_ids)
chat_ids = [1830477841]
announcement = "*Информатишка переезжает*\n" \
               "Мы решили изменить адрес бота на более подходящий \n" \
               "__По этому адресу бот прекращает работу__\n" \
               "Новый адрес: [@informatishka\_bot](https://t.me/informatishka_bot)\n "

announcement = get_announcement_from_markdown('data/announcements/1_migration.md')

@bot.message_handler(commands=['send_announcement'])
def send_announcement(message):
    for chat_id in chat_ids:
        bot.send_message(chat_id, announcement, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, 'Your announcement successfully sent')


if __name__ == '__main__':
    # send announcement once
    bot.polling(none_stop=True)
