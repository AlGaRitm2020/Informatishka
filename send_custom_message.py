import telebot
from config import TOKEN
from sql_work import get_all_users_chat_ids

bot = telebot.TeleBot(TOKEN)
chat_ids = [get_all_users_chat_ids()[3][0], get_all_users_chat_ids()[5][0]]
print(chat_ids)
announcement = "Test Announcement:\n" \
               "We have a new version of the Informatishka\n"


@bot.message_handler(commands=['send_announcement'])
def send_announcement(message):
    for chat_id in chat_ids:
        bot.send_message(chat_id, announcement)
    bot.send_message(message.chat.id, 'Your announcement successfully sent')


if __name__ == '__main__':
    # send announcement once
    bot.polling(none_stop=True)
