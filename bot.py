
#types of message

# text, audio, document, photo, sticker, video, video_note, voice, location, contact, new_chat_members, 
# left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, 
# channel_chat_created, migrate_to_chat_id, migrate_from_chat_id, pinned_message

import telebot
import requests
# import markups as m
from datetime import datetime
from flask import Flask, jsonify, request

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)
# import parser

app = Flask(__name__)

login_data= {
    'username': '',
    'password': '',
}
#main variables
TOKEN = "5804287527:AAHS5NpknvEmZPqWYsgnB08Xk5XtvNlaR9I"

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global isRunning
    isRunning = False
    if not isRunning:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Бот запущен!')#, reply_markup=m.start_markup)
        # bot.register_next_step_handler(msg, askAge) #askSource
        isRunning = True

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if(text == "/generate_token"):
        gt_command_handler(message)
    print(chat_id)

def gt_command_handler(message):
    # text = message.text.lower()
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Напишите свой логин:')#, reply_markup=m.start_markup)
    bot.register_next_step_handler(msg, askLogin) #askSource
    # bot.send_message(chat_id, 'Простите, я вас не понял :(')



def askLogin(message):
    chat_id = message.chat.id
    login_data['username'] = message.text
    msg = bot.send_message(chat_id, 'Теперь пароль:')
    bot.register_next_step_handler(msg, askPassword)

def askPassword(message):
    chat_id = message.chat.id
    login_data['password'] = message.text
    generate_token(chat_id,)

def generate_token(chat_id):
    r = requests.api.post("https://factory-bot-site.herokuapp.com//api-token-auth/", data=login_data)
    if(r.status_code == 200):
        r2 = requests.api.post("https://factory-bot-site.herokuapp.com//api/token/", data=login_data)

        payload = dict(token=r.json()["token"],chat_id=chat_id)
        headers = {'Authorization': 'JWT ' + r2.json()['access']}
        # http://127.0.0.1:8000/api/bots/
        r3 = requests.api.post("https://factory-bot-site.herokuapp.com//api/bots/", headers=headers, data=payload)
        
        if(r3.status_code == 200):
            bot.send_message(chat_id, "Токен создан")
        elif(r3.status_code == 201):
            bot.send_message(chat_id, "Токен уже есть")
        else:
            bot.send_message(chat_id, "Токен не удалось создать")
    else:
        bot.register_next_step_handler(bot.send_message(chat_id, "Не получилось создать токен"), askPassword)

bot.polling(none_stop=True)
