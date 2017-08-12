# -*- coding: utf-8 -*-

import telebot
from telebot import types
from pprint import pprint
import datetime
import requests
import logging
import configparser
import paho.mqtt.client as mqtt

logging.getLogger("requests").setLevel(logging.WARNING)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


config = configparser.ConfigParser()
config.read('bot_home.ini')

bot = telebot.TeleBot(config['KEYS']['bot_api'])
admins = config['ADMINS']['admins'].split(',')

def isAdmin(message):
    return str(message.from_user.id) in admins

"""
def quizSiNo():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Si')
    itembtn2 = types.KeyboardButton('No')
    markup.row(itembtn1)
    markup.row(itembtn2)
    return markup

def save(message, m_type="text", img_path=""):
    fn = message.from_user.first_name
    ln = message.from_user.last_name
    un = message.from_user.username
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Qué hacés che, cómo va eso?")

# proyector_on - Encender proyector
@bot.message_handler(commands=['proyector_on'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':4,value:0}")
    bot.reply_to(message, "Encendiendo proyector")

# proyector_off - Apagar proyector
@bot.message_handler(commands=['proyector_off'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':4,value:1}")
    bot.reply_to(message, "Apangando proyector")

# luz_habitacion_on - Encender luces de la habitación
@bot.message_handler(commands=['luz_habitacion_on'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':5,value:0}")
    bot.reply_to(message, "Encendiendo luces de la habitación")

# luz_habitacion_off - Apagar luces de la habitación
@bot.message_handler(commands=['luz_habitacion_off'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':5,value:1}")
    bot.reply_to(message, "Apangando luces de la habitación")
    
# led_azul_on - Encender led azul de la habitación
@bot.message_handler(commands=['led_azul_on'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':3,value:0}")
    bot.reply_to(message, "Encendiendo led azul de la habitación")

# led_azul_off - Apagar led azul de la habitación
@bot.message_handler(commands=['led_azul_off'], func=isAdmin)
def send_welcome(message):
    mqtt_client.publish("thing/esp/set_d", "{'pin':3,value:1}")
    bot.reply_to(message, "Apangando led azul de la habitación")

"""
@bot.message_handler(func=isAdmin)
def doForAdmin(message):
    #print('es admin')
    #bot.send_message(message.chat.id, message.text)

    #markup = types.ReplyKeyboardHide(selective=False)
    #bot.send_message(message.chat.id, message, reply_markup=markup)
    #pprint(vars(message))
    #print(message)
    save(message)
    r = getRespuesta(message)
    if r != "":
        bot.send_message(message.chat.id, r)
    #print(message.from_user, message.text)

    #bot.send_message(message.chat.id, "Debería estar en la mulata?", reply_markup=quizSiNo())
    # reply message
    #bot.reply_to(message, message.text)


@bot.message_handler(content_types=['sticker'])
def echo_all(message):
    pprint(vars(message.sticker))
    pprint(vars(message.sticker.thumb))

    file_id = message.sticker.file_id
    file_info = bot.get_file(file_id)
    #pprint(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    mediaDir = "/tmp"
    filename ="%s/%s.%s"%(mediaDir,file_id,"webp")
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    save(message,m_type="sticker",img_path=filename)

@bot.message_handler(content_types=['photo'])
def echo_all(message):
    pprint(vars(message))
    #for p in message.photo:
    p = message.photo[-1]
    pprint(vars(p))
    file_id = p.file_id
    file_info = bot.get_file(file_id)
    #pprint(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    mediaDir = "/tmp"
    filename ="%s/%s.%s"%(mediaDir,file_id,"webp")
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    save(message,m_type="photo",img_path=filename)


@bot.message_handler()
def echo_all(message):
    #print(message)
    pass
    #print(message.from_user, message.text)
"""


mqtt_client = mqtt.Client()
#mqtt_client.on_connect = on_connect
#mqtt_client.on_message = on_message

mqtt_client.connect(config['MQTT']['host'], int(config['MQTT']['port']), 60)
mqtt_client.loop_start()

bot.polling()