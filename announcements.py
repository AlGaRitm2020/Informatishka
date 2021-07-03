import telebot
from config_old import TOKEN
from sql_work import get_all_users_chat_ids


def get_announcement_from_markdown(file):
    with open(file, mode='r', encoding='utf-8') as md:
        announcement = md.read().replace('<br>', '')
    return announcement


bot = telebot.TeleBot(TOKEN)

"""
    this code send announcements to all users 
    don't send to all users test messages
"""

# all user chat id's
chat_ids = [i[0] for i in get_all_users_chat_ids()]

# set your chat id to it and send a messages only to you
chat_ids = [1830477841]

announcement = get_announcement_from_markdown('data/announcements/1_migration.md')


@bot.message_handler(commands=['send_announcement'])
def send_announcement(message):
    for chat_id in chat_ids:
        bot.send_message(chat_id, announcement, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, 'Your announcement successfully sent')


if __name__ == '__main__':
    bot.polling(none_stop=True)
