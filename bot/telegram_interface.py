import telebot
from telebot import types
from config import Config, ConfigConstructor, ConfigOneMessage
from .functions_for_buttons import *
from class_lessons import *

bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

# Конфиг
config = ConfigConstructor()

markup = None

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
    # btn3 = types.KeyboardButton('Promt')
    # btn4 = types.KeyboardButton('Set tasks')
    # btn5 = types.KeyboardButton('Set constant promt')
    # btn6 = types.KeyboardButton('Set regex')
    # btn7 = types.KeyboardButton('Set symbols')
    # btn8 = types.KeyboardButton('Run')

    # markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, handle_message)




@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if isinstance(config, ConfigOneMessage):
        global config
        promt = message.text
        config.promt = promt
        response = run_ai(config)
        
        bot.send_message(message.chat.id, response, reply_markup=markup)
    if message.content_type == 'text':
        if message.text == 'ConfigOneMessage':
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'ConfigConstructor':
            config = Config()
            bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)
        elif message.text == 'State':
            bot.send_message(message.chat.id, config.__str__(), reply_markup=markup)
        elif message.text == 'Clear state':
            config = ConfigConstructor()
            bot.send_message(message.chat.id, 'Completed \n' + config.__str__(), reply_markup=markup)
        elif message.text == 'Check directorys':
            pass

        # elif message.text == 'Promt':
        #     bot.send_message(message.chat.id, 'Please enter the prompt: ', reply_markup=markup)
        #     bot.register_next_step_handler(message, promt_action)
        # elif message.text == 'Set tasks':
        #     bot.send_message(message.chat.id, 'Please enter the tasks: ', reply_markup=markup)
        #     bot.register_next_step_handler(message, set_tasks)
        # elif message.text == 'Set constant promt':
        #     bot.send_message(message.chat.id, 'Please enter the constant promt: ', reply_markup=markup)
        #     bot.register_next_step_handler(message, set_constant_promt)
        # elif message.text == 'Set regex':
        #     bot.send_message(message.chat.id, 'Please enter the regex: ', reply_markup=markup)
        #     bot.register_next_step_handler(message, set_regex)
        # elif message.text == 'Set symbols':
        #     bot.send_message(message.chat.id, 'Please enter the symbols: ', reply_markup=markup)
        #     bot.register_next_step_handler(message, set_symbols)
        # elif message.text == 'Run':
        #     bot.send_message(message.chat.id, 'Please wait...', reply_markup=markup)
        #     run(message)

@bot.message_handler(content_types=['document'])
def receive_document(message):
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

