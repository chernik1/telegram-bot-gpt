import telebot
import webbrowser
import sqlite3
import requests
import json
import math



bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

commands = {
    'commands_help': ['help'],
    'commands_start': ['start', 'main'],
    'commands_id': ['id'],
    'commands_site': ['site', 'website'],
}

# @bot.message_handler(content_types=['photo'])
# def get_photo(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     btn1 = telebot.types.InlineKeyboardButton('Go site', url='https://google.com')
#     btn2 = telebot.types.InlineKeyboardButton('Delete photo', callback_data='delete')
#     btn3 = telebot.types.InlineKeyboardButton('Change photo', callback_data='edit')
#     markup.row(btn1, btn2, btn3)
#     bot.reply_to(message, 'Nice photo!', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data == 'delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     elif callback.data == 'edit':
#         bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
# @bot.message_handler(commands=commands['commands_site'])
# def site(message):
#     webbrowser.open('https://google.com')
# @bot.message_handler(commands=commands['commands_help'])
# def help(message):
#     with open('Html/help.html', 'r', encoding='utf-8') as f:
#         bot.send_message(message.chat.id, f.read(), parse_mode='HTML')
@bot.message_handler(commands=commands['commands_start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton('Go site')
    btn2 = telebot.types.KeyboardButton('Delete photo')
    btn3 = telebot.types.KeyboardButton('Change photo')
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)

    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Go site':
        bot.send_message(message.chat.id, 'Go site')
    elif message.text == 'Delete photo':
        bot.send_message(message.chat.id, 'Delete photo')
    elif message.text == 'Change photo':
        bot.send_message(message.chat.id, 'Change photo')




# @bot.message_handler(commands=commands['commands_id'])
# def id(message):
#     bot.reply_to(message, f'Your id: {message.chat.id}')
# @bot.message_handler()
# def echo_all(message):
#     bot.send_message(message.chat.id, message.text)

def start_bot():
    bot.polling(none_stop=True)
