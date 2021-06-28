import telebot
from config import TOKEN
from sql_work import get_all_users_chat_ids

bot = telebot.TeleBot(TOKEN)
chat_ins = [i[0] for i in get_all_users_chat_ids()]
print(chat_ins)
chat_ids = [get_all_users_chat_ids()[3][0], get_all_users_chat_ids()[5][0]]
print(chat_ids)
announcement = "*Информатишка переезжает*\n" \
               "Мы решили изменить адрес бота на более подходящий \n" \
               "__По этому адресу бот прекращает работу__\n" \
               "Новый адрес: [@informatishka\_bot](https://t.me/informatishka_bot)\n " \



@bot.message_handler(commands=['send_announcement'])
def send_announcement(message):
    for chat_id in chat_ids:
        bot.send_message(chat_id, announcement, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, 'Your announcement successfully sent')


if __name__ == '__main__':
    # send announcement once
    bot.polling(none_stop=True)
