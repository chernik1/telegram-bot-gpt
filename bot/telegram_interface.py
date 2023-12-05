import telebot
from telebot import types
from config import Config, ConfigConstructor, ConfigOneMessage
from .functions_for_buttons import *
from class_lessons import *
import os
from tools.pdf_form.logic import is_form_new_pdf
from tools.ppt_form.logic import is_form_new_ppt
from tools.docx_form.logic import is_form_new_docx


bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

# Конфиг
config = ConfigConstructor()

markup = None
markup_config = None
file_add = ''

dict_lessons_short = {
    'm': Math,
    'p': Programming,
    'e': Economics,
    'h': History,
    'en': English,
    'b': Biology,
    'c': Chemistry,
    'ph': Physics,
    'bel': Belorussian,
    'ma': MathAnalysis,
    'mga': MathGeometryAndAlgebra,
}

@bot.message_handler(commands=['start', 'main'])
def start(message):
    global markup
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('State')
    btn2 = types.KeyboardButton('Clear state')
    btn3 = types.KeyboardButton('ConfigOneMessage')
    btn4 = types.KeyboardButton('ConfigConstructor')
    btn5 = types.KeyboardButton('Check directorys')
    btn6 = types.KeyboardButton('Menu config')
    btn7 = types.KeyboardButton('Menu file')

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)

def check_directorys(message):
    lesson = dict_lessons_short[message.text]

    for file in os.listdir(f'lessons/{lesson.directory}'):
        bot.send_message(message.chat.id, file, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message_file(message):
    if message.text == 'File add':
        bot.send_message(message.chat.id, 'Please send file')
        bot.register_next_step_handler(message, receive_document)
    elif message.text == 'Check text':
        file_path = rf'{file_add}'
        response = is_form_new_pdf(file_path, message.text)
        for resp in response:
            bot.send_message(message.chat.id, resp, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global config
    global markup_config

    if message.content_type == 'text':
        if message.text == 'ConfigOneMessage':
            config = ConfigOneMessage()
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'ConfigConstructor':
            config = ConfigConstructor()
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'State':
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'Clear state':
            config = ConfigConstructor()
            bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)
        elif message.text == 'Check directorys':
            try:
                bot.send_message(message.chat.id, f'Please enter the lesson short name: ', reply_markup=markup)
                bot.register_next_step_handler(message, check_directorys)
            except:
                bot.send_message(message.chat.id, 'Ошибка в ведение имени директории', reply_markup=markup)
        elif message.text == 'Menu config':
            btn1 = types.KeyboardButton('Constant promt')
            btn2 = types.KeyboardButton('Tasks')
            btn3 = types.KeyboardButton('Regex promt')
            btn4 = types.KeyboardButton('Symbols')
            btn5 = types.KeyboardButton('Run')
            markup = types.ReplyKeyboardMarkup()
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(message.chat.id, 'Menu config', reply_markup=markup)
        elif message.text == 'Menu file':
            btn1 = types.KeyboardButton('File add')
            btn2 = types.KeyboardButton('Check text')
            markup = types.ReplyKeyboardMarkup()
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Menu file', reply_markup=markup)
        elif isinstance(config, ConfigOneMessage):
            promt = message.text
            config.promt = promt
            response = run_ai(config)

            bot.send_message(message.chat.id, response, reply_markup=markup)

@bot.message_handler(content_types=['document'])
def receive_document(message):
    global file_add
    if message.caption:
        flag = False
        try:
            lesson = dict_lessons_short[message.caption.split()[0].lower()]
            flag = True
        except:
            print('Предмет не найден')

        if flag:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(lesson.directory, message.document.file_name)
            with open(f'lessons/{lesson.directory}/{message.document.file_name}', 'wb') as new_file:
                new_file.write(downloaded_file)

            file_add = f'lessons/{lesson.directory}/{message.document.file_name}'
            file_format = file_add.split('.')[-1]
            if file_format == 'pdf':
                response = is_form_new_pdf(file_add, message.text)
                for resp in response:
                    bot.send_message(message.chat.id, resp, reply_markup=markup)
            elif file_format == 'docx':
                response = is_form_new_docx(file_add, message.text)
                for resp in response:
                    bot.send_message(message.chat.id, resp, reply_markup=markup)
            elif file_format == 'txt':
                response = is_form_new_txt(file_add, message.text)
                for resp in response:
                    bot.send_message(message.chat.id, resp, reply_markup=markup)


    bot.reply_to(message, 'File received')

@bot.message_handler(content_types=['photo'])
def receive_photo(message):

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(rf'{1}', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, 'Photo received')

def start_bot():
    bot.polling(none_stop=True)

