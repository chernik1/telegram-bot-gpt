import telebot
from telebot import types
from config import Config
import os
from tools.pdf_form.logic import is_form_new_pdf
from tools.ai.logic import run_ai
import re
import sqlite3
import time
# from tools.ppt_form.logic import is_form_new_ppt
# from tools.docx_form.logic import is_form_new_docx

# ToDo: вывод

bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

# Конфиг
config = Config()

markup = None
markup_config = None
file_add = ''

# Глобальная переменная для хранения текста из предыдущего сообщения
previous_text = ''

@bot.message_handler(commands=['start', 'main'])
def start(message):
    """Функция запуска интерфейса для пользователя"""
    global markup
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('help')

    markup.add(btn1)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)


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
    global previous_text

    if message.content_type == 'text':
        if config.db_action_for_lesson:
            list_numbers = message.text.split()
            time.sleep(10)
            for i in range(len(list_numbers)):
                with open(f'bot/response_{list_numbers[i]}.txt', 'r', encoding='utf-8') as file:
                    response_full = file.read()
                response__split_3999 = [response_full[i:i + 3888] for i in range(0, len(response_full), 3888)]
                for response in response__split_3999:
                    bot.send_message(message.chat.id, str(list_numbers[i]) + response, reply_markup=markup)
        elif message.text[:7] == 'answer ' and len(message.text.split('***')) == 2:
            message.text = message.text[7:]
            info = message.text.split('***')
            lesson = info[0]
            answer_id = int(info[1])

            db = sqlite3.connect(r'db/database.db')
            cur = db.cursor()
            cur.execute(f"""SELECT answer FROM lessons WHERE name_lesson = '{lesson + "_" + str(answer_id)}'""")
            answer = cur.fetchall()
            db.close()

            bot.send_message(message.chat.id, answer[0][0], reply_markup=markup)

        elif message.text[:7] == 'prompt ' and len(message.text.split('***')) == 3:

            message.text = message.text[7:]
            info = message.text.split('***')
            config.lesson = info[0]
            config.tasks = info[1]
            config.prompt_constant = info[2]

            responses_status = run_ai(config)

            responses = responses_status[0]
            status = responses_status[1]
            const_num = 73
            if status:
                for id, response in enumerate(responses, const_num):
                    # bot.send_message(message.chat.id, response, reply_markup=markup)

                    with open(f'G:\\telegram-bot-gpt\\bot\\response_{id}.txt', 'a+', encoding='utf-8') as file:
                        file.write(response)

                    # db = sqlite3.connect(r'db/database.db')
                    # cur = db.cursor()
                    #
                    # existing_lesson = cur.execute(f"""SELECT name_lesson FROM lessons WHERE name_lesson = ?""",
                    #                               (info[0] + '_',)).fetchone()
                    #
                    # if existing_lesson:
                    #     print('Уже есть')
                    # else:
                    #     # Выполните вставку новой записи
                    #     cur.execute(f"""INSERT INTO lessons(name_lesson, id_question, answer) VALUES(?, ?, ?)""",
                    #                 (info[0] + '_' + str(id), id, response))
                    #     db.commit()
                    #
                    # db.close()
                bot.send_message(message.chat.id, 'Готово', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Ошибка', reply_markup=markup)
        elif message.text[:7] == 'prompt ' and len(message.text.split('***')) == 2:
            message.text = message.text[7:]
            info = message.text.split('***')
            tasks = info[0]
            prompt_constant = info[1]

            responses_status = run_ai(config)
            responses = responses_status[0]
            status = responses_status[1]

            if status:
                for id, response in enumerate(responses, 1):
                    bot.send_message(message.chat.id, str(id) + ' ' + response, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Ошибка', reply_markup=markup)


        elif message.text[:7] == 'delete ' and len(message.text.split('***')) == 2:
            message.text = message.text[7:]
            info = message.text.split('***')
            lesson = info[0]
            prompt = info[1]
            db = sqlite3.connect(r'db/database.db')
            cur = db.cursor()
            if prompt == 'all':
                cur.execute(f"""DELETE FROM lessons WHERE name_lesson LIKE '{lesson}%'""")
            else:
                cur.execute(f"""DELETE FROM lessons WHERE name_lesson = '{lesson + "_" + str(prompt)}'""")
            db.commit()
            db.close()
            bot.send_message(message.chat.id, 'Удалено', reply_markup=markup)
        elif message.text.lower() == 'help':
            bot.send_message(message.chat.id, """
                    Help
Обычный запрос - prompt tasks***prompt_constant
Запрос о предмете - prompt lesson***tasks***prompt_constant
Удаление запроса - delete lesson***prompt
Получить вопрос для определенного предмета - action lesson
Остановить запрос для определенного предмета - clear action
            """, reply_markup=markup)
            bot.send_message(message.chat.id, f'{config.__str__()}', reply_markup=markup)
        elif message.text.lower()[:7] == 'action ':
            message.text = message.text[7:]
            info = message.text.split()
            config.db_action_for_lesson = True
            config.lesson = info[0]
            bot.send_message(message.chat.id, f'Запрос для {config.lesson} установлен', reply_markup=markup)
        elif message.text.lower() == 'clear action':
            config.db_action_for_lesson = False
            bot.send_message(message.chat.id, f'Запрос очищен', reply_markup=markup)

@bot.message_handler(content_types=['document'])
def receive_document(message):
    """Функция получения файла"""
    global file_add
    if message.caption:
        flag = False
        if flag:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'{message.document.file_name}', 'wb') as new_file:
                new_file.write(downloaded_file)

            file_add = f'{message.document.file_name}'
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

