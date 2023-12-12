import telebot
from telebot import types
from config import Config, ConfigConstructor, ConfigOneMessage
from class_lessons import *
import os
from tools.pdf_form.logic import is_form_new_pdf
from tools.ai.logic import start_ai
import re
# from tools.ppt_form.logic import is_form_new_ppt
# from tools.docx_form.logic import is_form_new_docx


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
    """Функция запуска интерфейса для пользователя"""
    global markup
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('help')

    markup.add(btn1)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)

def check_directorys(message):
    """Функция проверки директорий"""
    lesson = dict_lessons_short[message.text]

    for file in os.listdir(rf'{config.directory}/{lesson.directory}'):
        bot.send_message(message.chat.id, file, reply_markup=markup)


# @bot.message_handler(func=lambda message: True)
# def handle_message_file(message):
#     if message.text == 'File add':
#         bot.send_message(message.chat.id, 'Please send file')
#         bot.register_next_step_handler(message, receive_document)
#     elif message.text == 'Check text':
#         file_path = rf'{file_add}'
#         response = is_form_new_pdf(file_path, message.text)
#         for resp in response:
#             bot.send_message(message.chat.id, resp, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Функция обработки сообщений"""
    global config
    global markup_config

    if message.content_type == 'text':
        if message.text[:6] == 'promt ' and len(message.text.split('***')) == 3:
            pass
        elif message.text[:6] == 'promt ':
            message.text = message.text[6:]
            info = message.text.split('***')
            config.tasks = info[0]
            config.promt_constant = info[1]
            if len(info) > 2:
                config.symbols = info[2]
            responses, status = run_ai(config)
            if status:
                for index, response in enumerate(responses, 1):
                    with open(rf'{index}.txt', 'a+', encoding='utf-8') as file:
                        file.write(f'{index} {response}\n')
                    bot.send_message(message.chat.id, 'ок')
        elif message.text.lower() == 'help':
            bot.send_message(message.chat.id, """
                    Help
Обычный запрос - promt tasks***promt_constant
Запрос о предмете - promt lesson***tasks***promt_constant
            """, reply_markup=markup)

@bot.message_handler(content_types=['document'])
def receive_document(message):
    """Функция получения файла"""
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
            # elif file_format == 'docx':
            #     response = is_form_new_docx(file_add, message.text)
            #     for resp in response:
            #         bot.send_message(message.chat.id, resp, reply_markup=markup)
            # elif file_format == 'pptx':
            #     response = is_form_new_ppt(file_add, message.text)
            #     for resp in response:
            #         bot.send_message(message.chat.id, resp, reply_markup=markup)


    bot.reply_to(message, 'File received')

@bot.message_handler(content_types=['photo'])
def receive_photo(message):
    """Функция получения фото"""
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(rf'{1}', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, 'Photo received')

def start_bot():
    """Функция запуска бота"""
    bot.polling(none_stop=True)

