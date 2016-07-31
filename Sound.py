import telebot
from telebot import types
import requests
import geocoder
import pyowm
import soundcloud
import random


API_TOKEN_MAIN_MUZIS = '231161869:AAFpafehgQl9V-5f6-1KvwjPkzhbgdqDflU'
owm = pyowm.OWM('2d5a653b91e72adfe96cbe71f279fb85')

bot_muzis = telebot.TeleBot(API_TOKEN_MAIN_MUZIS)

@bot_muzis.message_handler(commands=["random"])
def random_music(message):

    # create a client object with your app credentials
    client = soundcloud.Client(client_id='5011e3c314883958b531b8cfde500751')
    n = random.randint(-1, 4)
    track = ['nelson-jaee-loyalty', '293', 'fetty-wap-wake-up',
             'famous-dex-what-got-into-me', 'famous-dex-ok-dexter']
    if n == -1:
        bot_muzis.send_message(message.chat.id, 'http://f.muzis.ru/p08vf5c9fl1q.mp3')
    else:

        track = client.get('/tracks/' + track[n])
    # get the tracks streaming URL
        stream_url = client.get(track.stream_url, allow_redirects=False)

    # print the tracks stream URL
        bot_muzis.send_message(message.chat.id, stream_url.location)


@bot_muzis.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot_muzis.send_message(message.chat.id, 'http://bit.ly/2ai4Zax')


@bot_muzis.message_handler(content_types=["location"])
def repeat_all_messages1(message):  #
    k = ""
    k1 = ""
    s = str(message.location)
    t = True
    n = 0
    for i in s:
        n +=1
        if((i == "." or i.isdigit()) and t):
          k += i
        if(i == ","):
            t = False
        if (not t) and (i == "." or i.isdigit()):
            k1 +=i
    print(k)
    print(k1)
    bot_muzis.send_message(message.chat.id, "hiiii 😅😅😅😅" + str(message.location))
    g = str(message.location)
    print(g)
    loc = []
    loc.append(float(k1))
    loc.append(float(k))
    forecast = owm.daily_forecast("Milan,it")
    tomorrow = pyowm.timeutils.tomorrow()
    forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

    # Search for current weather in London (UK)
    observation = owm.weather_at_place('London,uk')
    w = observation.get_weather()
    print(w)
    g = geocoder.google(loc, method = 'reverse')
    bot_muzis.send_message(message.chat.id, "hiiii 😅😅😅😅" + str(g.state))


if __name__ == '__main__':
    bot_muzis.polling(none_stop=True)
