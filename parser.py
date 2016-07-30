import re
from datetime import datetime
import telebot
from telebot import types
import datetime
from telebot import types

API_TOKEN = '245708423:AAFPl1DZrUFrNiH-0FhFtxr4ZDEll0ukEsQ'
bot = telebot.TeleBot(API_TOKEN)

hello = ['привет', 'здравствуй', 'здравствуйте', 'hello', 'приветствую']


class Request:
    artist = ''
    album = ''
    date = 0

    def show(self):
        return 'sample text'


key_words = ['последний', 'последние', 'последняя',
             'топ', 'лучший', 'лучшие', 'лучшая',
             'трек', 'песня', 'трэк',
             'альбом', 'сингл']


# the Levenstein distance algorithm
def distance(a: object, b: object) -> object:
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main_func(s):
    user_request = Request()
    s = re.sub(r'[^\w\s]', '', s)
    s_splitted = s.split()
    for _ in range(len(s_splitted)):
        s_splitted[_] = s_splitted[_].lower()
        if represents_int(s_splitted[_]):
            if 1990 < s_splitted < 2016:
                user_request.date = int(s_splitted[_])
                s_splitted.pop(_)
    return s_splitted


def check_hello(s):
    for _ in range(len(hello)):
        if hello[_] in main_func(s):
            print('Добрейший вечерочек!')
            break
    check_daytime()


def check_daytime():
    now = datetime.datetime.now().hour
    print(now)
    if 0 <= now <= 5:
        print('у меня есть плейлист для этой ночи!')
    elif 5 < now < 12:
        print('надеюсь, это утро у вас проходит хорошо. почему бы не послушать этот плейлист?')
    elif 12 <= now <= 18:
        print('надеюсь, этот день у вас проходит хорошо. почему бы не послушать этот плейлист?')
    else:
        print('надеюсь, этот вечер у вас проходит хорошо. почему бы не послушать этот плейлист?')


@bot.message_handler(content_types=['text'])
def answer_message(message):
    
    keyboard = types.InlineKeyboardMarkup()
    like_button = types.InlineKeyboardButton('LIKE', callback_data='1')
    not_sure_button = types.InlineKeyboardButton('NOT SURE...', callback_data='2')
    dislike_button = types.InlineKeyboardButton('DISLIKE', callback_data='3')
    keyboard.add(dislike_button, not_sure_button, like_button)
    bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == '1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Спасибо! Мы больше не будет отправлять вам этот трек')
        if call.data == '2':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=None)
        if call.data == '3':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Спасибо за отзыв')
if __name__ == '__main__':
    bot.polling(none_stop=True)
