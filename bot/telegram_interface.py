import telebot
from telebot import types
from config import Config
import os
from tools.ai.logic import run_ai
import re
import sqlite3
import time

bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

import string

alphabet = string.ascii_lowercase

@bot.message_handler(commands=['start', 'main'])
def start(message):
    """Функция запуска интерфейса для пользователя"""
    global markup
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('/help')
    btn2 = types.KeyboardButton('/config')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Функция обработки сообщений"""
    global config

    if message.content_type == 'text':
        if config.db_action_for_multitask and any(not char.isalpha() or char.lower() not in alphabet for char in message.text):
            list_numbers = message.text.split()
            time.sleep(10)
            for i in range(len(list_numbers)):
                with open(f'bot/response_{list_numbers[i]}.txt', 'r', encoding='utf-8') as file:
                    response_full = file.read()
                response__split_3999 = [response_full[i:i + 3888] for i in range(0, len(response_full), 3888)]
                for response in response__split_3999:
                    bot.send_message(message.chat.id, str(list_numbers[i]) + response, reply_markup=markup)
        elif message.text.lower() == 'help':
                bot.send_message(message.chat.id, """
                            Help
        Обычный запрос - /prompt или /pr tasks***prompt_constant
        Запрос о предмете - /prompt или /pr pack***tasks***prompt_constant
        Удаление запроса - /delete или /del pack***prompt
        Получить вопрос для определенного предмета - /action или /act pack
        Остановить запрос для определенного предмета - /cl ac или /clear action
        Конфигурация - /config или /cfg
        Установить regex - /set regex выражение
                    """, reply_markup=markup)
                bot.send_message(message.chat.id, f'{config.__str__()}', reply_markup=markup)
        elif (message.text[:4] == '/ans' or message.text[:7] == '/answer') and len(message.text.split('***')) == 2:
            message.text = message.text[4:]
            info = message.text.split('***')
            name_multitask = info[0]
            answer_id = int(info[1])

            db = sqlite3.connect(r'db/database.db')
            cur = db.cursor()
            cur.execute(f"""SELECT answer FROM multitask WHERE name_multitask = '{name_multitask + "_" + str(answer_id)}'""")
            answer = cur.fetchall()
            db.close()

            bot.send_message(message.chat.id, answer[0][0], reply_markup=markup)

        elif (message.text[:3] == '/pr' or message.text[:7] == '/prompt') and len(message.text.split('***')) == 3 and not config.flag_question:

            message.text = message.text[3:]
            info = message.text.split('***')
            config.name_pack = info[0]
            config.tasks = info[1]
            config.prompt_constant = info[2]

            responses_status = run_ai(config)

            responses = responses_status[0]
            status = responses_status[1]
            answer = responses_status[2]
            const_num = 1
            if status:
                for id, response in enumerate(responses, const_num):

                    db = sqlite3.connect(r'db/database.db')
                    cur = db.cursor()

                    existing_name_pack = cur.execute(f"""SELECT name_pack FROM multitask WHERE name_multitask = ?""",
                                                  (info[0] + '_',)).fetchone()

                    if existing_name_pack:
                        print('Уже есть')
                    else:
                        # Выполните вставку новой записи
                        cur.execute(f"""INSERT INTO pack(name_multitask, answer, question) VALUES(?, ?, ?)""",
                                    (info[0] + '_' + str(id), response, answer))
                        db.commit()

                    db.close()

                bot.send_message(message.chat.id, 'Готово')
            else:
                bot.send_message(message.chat.id, 'Ошибка', reply_markup=markup)
        elif (message.text[:3] == '/pr' or message.text[:7] == '/prompt') and len(message.text.split('***')) == 2:
            message.text = message.text[3:]
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
        elif (message.text[:4] == '/del' or message.text[:7] == '/delete') and len(message.text.split('***')) == 2:
            message.text = message.text[4:]
            info = message.text.split('***')
            name_multitask = info[0]
            prompt = info[1]
            db = sqlite3.connect(r'db/database.db')
            cur = db.cursor()
            if prompt == 'all':
                cur.execute(f"""DELETE FROM multitask WHERE name_multitask LIKE '{name_multitask}%'""")
            else:
                cur.execute(f"""DELETE FROM multitask WHERE name_multitask = '{name_multitask + "_" + str(prompt)}'""")
            db.commit()
            db.close()
            bot.send_message(message.chat.id, 'Удалено', reply_markup=markup)
        elif message.text.lower()[:4] == '/act' or message.text.lower()[:7] == '/action':
            message.text = message.text[7:]
            info = message.text.split()
            config.db_action_for_pack = True
            config.name_pack = info[0]
            bot.send_message(message.chat.id, f'Запрос для {config.name_pack} установлен', reply_markup=markup)
        elif message.text.lower() == '/clear action' or message.text.lower() == '/cl ac':
            config.db_action_for_pack = False
            bot.send_message(message.chat.id, f'Запрос очищен', reply_markup=markup)
        elif message.text.lower() == '/config' or message.text.lower() == '/cfg':
            bot.send_message(message.chat.id, f'{config.__str__()}', reply_markup=markup)
        elif message.text.lower() == '/set regex':
            message.text = message.text[10:].strip()
            config.regex = message.text
            bot.send_message(message.chat.id, f'Регулярное выражение установлено', reply_markup=markup)
        elif message.text.lower() == '/flag':
            config.flag_question = not config.flag_question
            bot.send_message(message.chat.id, f'Флаг {config.flag_question}', reply_markup=markup)

def start_bot():
    """Функция запуска бота"""
    global config, markup

    config = Config()
    markup = types.ReplyKeyboardMarkup()

    bot.polling(none_stop=True)


