import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
chat_id = 1283628271


announcement = "Announcement:\n" \
                "lorem fadfasdfas\n" \
                "dfasdfasdfa\n" \
                "sdfasdfasdfasdf\n" \
                "asdfasdfadsfasfd\n"

@bot.message_handler(commands=['send_announcement'])
# Объявляем функцию
def send_announcement(message):
    bot.send_message(chat_id,  announcement)
    bot.send_message(message.chat.id, 'Your announcement successfully sent')


if __name__ == '__main__':
    bot.polling(none_stop=True)
