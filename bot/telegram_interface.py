import telebot
from telebot import types
from ai.logic import run_ai
from config import Config

bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

# Конфиг
config = Config()


@bot.message_handler(commands=['start', 'main'])
def start(message):
    global markup
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('State')
    btn2 = types.KeyboardButton('Clear state')
    btn3 = types.KeyboardButton('Promt')
    btn4 = types.KeyboardButton('Set tasks')
    btn5 = types.KeyboardButton('Set constant promt')
    btn6 = types.KeyboardButton('Set regex')
    btn7 = types.KeyboardButton('Set symbols')
    btn8 = types.KeyboardButton('Run')

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)

def promt_action(message):
    global config

    config.promt = message.text

    responses, status = run_ai(config)

    for response in responses:
        bot.send_message(message.chat.id, response, reply_markup=markup)


def set_tasks(message):
    global config
    config.tasks = message.text
    bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)

def set_constant_promt(message):
    global config
    config.promt_constant = message.text
    bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)

def set_regex(message):
    global config
    config.regex = message.text
    bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)

def set_symbols(message):
    global config
    config.symbols = message.text
    bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)

def run(message):
    global config
    responses, status = run_ai(config)

    for response in responses:
        bot.send_message(message.chat.id, response, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global config
    if message.content_type == 'text':
        if message.text == 'State':
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'Clear state':
            config = Config()
            bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)
        elif message.text == 'Promt':
            bot.send_message(message.chat.id, 'Please enter the prompt: ', reply_markup=markup)
            bot.register_next_step_handler(message, promt_action)
        elif message.text == 'Set tasks':
            bot.send_message(message.chat.id, 'Please enter the tasks: ', reply_markup=markup)
            bot.register_next_step_handler(message, set_tasks)
        elif message.text == 'Set constant promt':
            bot.send_message(message.chat.id, 'Please enter the constant promt: ', reply_markup=markup)
            bot.register_next_step_handler(message, set_constant_promt)
        elif message.text == 'Set regex':
            bot.send_message(message.chat.id, 'Please enter the regex: ', reply_markup=markup)
            bot.register_next_step_handler(message, set_regex)
        elif message.text == 'Set symbols':
            bot.send_message(message.chat.id, 'Please enter the symbols: ', reply_markup=markup)
            bot.register_next_step_handler(message, set_symbols)
        elif message.text == 'Run':
            bot.send_message(message.chat.id, 'Please wait...', reply_markup=markup)
            run(message)

def start_bot():
    bot.polling(none_stop=True)

