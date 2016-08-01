import re
from datetime import datetime
import telebot
from telebot import types
import datetime
import soundcloud
import random
import sqlite3

API_TOKEN = '245708423:AAFPl1DZrUFrNiH-0FhFtxr4ZDEll0ukEsQ'
bot = telebot.TeleBot(API_TOKEN)

hello = ['привет', 'здравствуй', 'здравствуйте', 'hello', 'приветствую', 'шалом', 'ассалам алейкум']
cafe = ['кафе', 'ресторан', 'ресторане']
metro = ['метро', 'подземка', 'подземку']
hackathon = ['хакатон', 'хакатоне', 'хакатону', 'хакатоном']
kind_of_music = ['энергичная', 'спокойная', 'тихая', 'громкая', 'интенсивная', 'классическая','классика', 'академическая', 'странная', '']


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
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)
    s_splitted = s.split()
    return s_splitted


def check_hello(s):
    for _ in range(len(hello)):
        if hello[_] in main_func(s):
            return True
            break
        else: return False
    check_daytime()


def check_cafe(s):
    for _ in range(len(cafe)):
        if cafe[_] in main_func(s):
            return True
            break
        else: return False


def check_metro(s):
    for _ in range(len(metro)):
        if metro[_] in main_func(s):
            return True
            break
        else: return False


def check_hackathon(s):
    for _ in range(len(hackathon)):
        if hackathon[_] in main_func(s):
            return True
            break
        else: return False


def check_daytime():
    now = datetime.datetime.now().hour
    if 0 <= now <= 5:
        return 'night'
    elif 5 < now < 12:
        return 'morning'
    elif 12 <= now <= 18:
        return 'day'
    else:
        return 'evening'


def check_kind_of_music(s):
    i = 0
    index_of_the_most_likely_variant = -1
    min_value = 255
    for _ in range(len(kind_of_music)):
        for k in range(len(main_func(s))):
            if distance(main_func(s)[k], kind_of_music[_]) < 3:
                min_value = distance(main_func(s)[k], kind_of_music[_])
                index_of_the_most_likely_variant = i
        i += 1
    return kind_of_music[index_of_the_most_likely_variant]



keyboard = types.InlineKeyboardMarkup()
like_button = types.InlineKeyboardButton('👍', callback_data='1')
not_sure_button = types.InlineKeyboardButton('🤔', callback_data='2')
dislike_button = types.InlineKeyboardButton('👎', callback_data='3')
keyboard.add(like_button, not_sure_button, dislike_button)

@bot.message_handler(commands=["top3"])
def return_top(message):
    for i in range(3):
        n = random.randint(0, 8)
        client = soundcloud.Client(client_id='5011e3c314883958b531b8cfde500751')
        track = client.get('/tracks/' + calm[n])
        # get the tracks streaming URL
        stream_url = client.get(track.stream_url, allow_redirects=False)
        bot.send_message(message.chat.id, stream_url.location)
        bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)

@bot.message_handler(commands=["delivery"])
def delivery(message):
    bot.send_message(message.chat.id, "Вы подписались на нашу рассылочку, теперь мы будем делать для вас музыкальную подборку каждый день в 20:00 по Москве."
                                      "Отписаться можно с помощью команды /deliveryoff.")

@bot.message_handler(commands=["deliveryoff"])
def delivery(message):
    bot.send_message(message.chat.id, "Вы отписались от «Muzis». Вернуть подписку можно в любой момент с помощью команды /delivery")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    list_of_commands = '''Список команд:\n/random — случайный трек\n/top3 — 3 лучших трека недели\n/delivery — включить подписку\n/help — получить список команд бота'''
    bot.send_message(message.chat.id, list_of_commands)
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text='Hackathon по чатботам и AI', url='http://hackathon.muzis.ru')
    keyboard.add(url_button)
    bot.send_message(message.chat.id, 'Больше информации о хакатоне:', reply_markup=keyboard)


@bot.message_handler(commands=["random"])
def random_music(message):

    # create a client object with your app credentials
    client = soundcloud.Client(client_id='5011e3c314883958b531b8cfde500751')
    n = random.randint(-1, 4)
    track = ['nelson-jaee-loyalty', '293', 'fetty-wap-wake-up',
             'famous-dex-what-got-into-me', 'famous-dex-ok-dexter']
    if n == -1:
        bot.send_message(message.chat.id, 'http://f.muzis.ru/p08vf5c9fl1q.mp3')
    else:

        track = client.get('/tracks/' + track[n])
    # get the tracks streaming URL
        stream_url = client.get(track.stream_url, allow_redirects=False)

    # print the tracks stream URL
        bot.send_message(message.chat.id, stream_url.location)

@bot.message_handler(commands=['start'])
def gen_user(message):
    bot.send_message(message.chat.id,
                     "Ок, мы рады, что вы присоединились к нам. Выбирайте музыку и в скором времени мы сможем подстраиваться под ваши вкусы."
                     )
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    #cur.execute("CREATE  TABLE  users (id INTEGER PRIMARY KEY, userid INTEGER, j1 INTEGER, j2 INTEGER, j3 INTEGER, j4 INTEGER, j5 INTEGER)")
    #con.commit()
    """
    cur.execute("SELECT rowid FROM users WHERE userid = " + str(message.chat.id))
    k = cur.fetchall()
    if len(k) != 0:
        bot.send_message(message.chat.id, "Мы уже начали составлять ваш уникальный плейлист.Использование команды еще раз /start сотрет всю нашу информацию о вас."
                                               "Вы уверены, что хотите это сделать ? ")
        markup = types.ReplyKeyboardMarkup()
        markup.row('да')
        markup.row('нет')
        bot.send_message(message.chat.id, "Выбирайте:", reply_markup=markup)
    else:
    """
    s_main = "INSERT INTO users (id, userid, j1, j2, j3, j4, j5) VALUES(NULL, " + \
                str(message.chat.id) + ", \"" + str(0) + "\", \"" + str(0) + "\", \"" + str(0) + "\", \"" + str(
            0) + "\", \"" + str(0) + "\")"

    cur.execute(s_main)
    con.commit()
    con.close()

@bot.message_handler(commands=['reset'])
def reset_row(message):
    bot.send_message(message.chat.id, "Ок. Пусть это останется на вашей совести. Начните с комманды /start и мы составим для вас еще более персонализированный набор музыки")
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE userid = " + str(message.chat.id))
    con.commit()
    con.close()
@bot.message_handler(content_types=['text'])
def rate_the_song(message):
    """
    markup = types.ReplyKeyboardHide()

    if message.text == "да":
        bot.send_message(message.chat.id, 'Ок. Пусть это останется на вашей совести. Начните с комманды /start и мы составим для вас еще более персонализированный набор музыки', reply_markup=markup)
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE userid = "  + str(message.chat.id))
        con.commit()
        con.close()
    if message.text == "нет":
        bot.send_message(message.chat.id, 'Хорошо, просто забудем это!', reply_markup=markup)
        """
    client = soundcloud.Client(client_id='5011e3c314883958b531b8cfde500751')
    n = random.randint(0, 8)
    track = client.get('/tracks/' + calm[n])
    # get the tracks streaming URL
    stream_url = client.get(track.stream_url, allow_redirects=False)

    # print the tracks stream URL


    if check_hello(message.text):
        bot.send_message(message.chat.id, 'Привет!')
        if check_daytime() == 'night':
            bot.send_message(message.chat.id, 'Для этой ночи я подготовил такой плейлист:')
            bot.send_message(message.chat.id, stream_url.location)
            bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)

        if check_daytime() == 'morning':
            bot.send_message(message.chat.id, 'Доброе утро! Вот твой сегодняшний плейлист:')
            bot.send_message(message.chat.id, stream_url.location)
            bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
        if check_daytime() == 'day':
            bot.send_message(message.chat.id, 'Доброго дня! Вот твой плейлист на сегодня:')
            bot.send_message(message.chat.id, stream_url.location)
            bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
        if check_daytime() == 'evening':
            bot.send_message(message.chat.id, 'Этим вечером тебе определённо понравится послушать это:')
            bot.send_message(message.chat.id, stream_url.location)
            bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
    elif check_cafe(message.text):
        bot.send_message(message.chat.id, 'У меня как раз есть плейлист для кафе!')
        bot.send_message(message.chat.id, stream_url.location)
        bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
    elif check_metro(message.text):
        bot.send_message(message.chat.id, 'С этим плейлистом время в метро пройдет быстрее:')
        bot.send_message(message.chat.id, stream_url.location)
        bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
    elif check_hackathon(message.text):
        bot.send_message(message.chat.id,
                         'С этим плейлистом на хакатоне будет веселее и работа, надеюсь, пойдет продуктивнее:')
        bot.send_message(message.chat.id, stream_url.location)
        bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
    elif check_kind_of_music(message.text) != '':
        bot.send_message(message.chat.id, 'Вас интересует ' + check_kind_of_music(message.text) + ' музыка?')
        bot.send_message(message.chat.id, stream_url.location)
        bot.send_message(message.chat.id, 'Оцените песню: ', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Мы вас не поняли((")

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
