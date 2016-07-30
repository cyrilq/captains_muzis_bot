import re
from datetime import datetime
import telebot
from telebot import types
import datetime

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
    s = re.sub(r'[^\w\s]', '', s).lower()
    s_splitted = s.split()
    return s_splitted


def check_hello(s):
    for _ in range(len(hello)):
        if hello[_] in main_func(s):
            return True
            break
        else: return False
    check_daytime()


def check_daytime():
    now = datetime.datetime.now().hour
    print(now)
    if 0 <= now <= 5:
        return 'night'
    elif 5 < now < 12:
        return 'morning'
    elif 12 <= now <= 18:
        return 'day'
    else:
        return 'evening'


@bot.message_handler(content_types=['text'])
def rate_the_song(message):
    try:
        if check_hello(message.text):
            bot.send_message(message.chat.id, 'Привет!')
            if check_daytime() == 'night':
                bot.send_message(message.chat.id, 'Для этой ночи я подготовил такой плейлист:')
            if check_daytime() == 'morning':
                bot.send_message(message.chat.id, 'Доброе утро! Вот твой сегодняшний плейлист:')
            if check_daytime() == 'day':
                bot.send_message(message.chat.id, 'Доброго дня! Вот твой плейлист на сегодня:')
            if check_daytime() == 'evening':
                bot.send_message(message.chat.id, 'Этим вечером тебе определённо понравится послушать это:')
    except: print('Что-то пошло не так...')
    keyboard = types.InlineKeyboardMarkup()
    like_button = types.InlineKeyboardButton('👍', callback_data='1')
    not_sure_button = types.InlineKeyboardButton('🤔', callback_data='2')
    dislike_button = types.InlineKeyboardButton('👎', callback_data='3')
    keyboard.add(like_button, not_sure_button, dislike_button)
    bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == '1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Спасибо за отзыв 😉')
        if call.data == '2':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Спасибо за отзыв')
        if call.data == '3':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Спасибо! Мы больше не будет отправлять вам этот трек')
if __name__ == '__main__':
    bot.polling(none_stop=True)


@bot.message_handler(commands='help')
def send_welcome(message):
    list_of_commands = '''Список команд:\n/random — случайный трек\n/top3 — 3 лучших трека недели\n/top5 — 5 лучших треков недели\n/delivery — включить подписку\n'''
    bot.send_message(message.chat.id, list_of_commands)
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text='Конкурс BudgetApps', url='http://budgetapps.ru/contest')
    keyboard.add(url_button)
