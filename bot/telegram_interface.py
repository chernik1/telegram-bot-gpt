import telebot
from telebot import types
from ai.logic import run_ai

bot = telebot.TeleBot('6417218112:AAEQmNzdBVw9fpVAXFAjqwjIvcDUtH93Xt8')

# Определение состояний
states = {}

@bot.message_handler(commands=['start', 'main'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Set regex', callback_data='set_regex')
    btn2 = types.InlineKeyboardButton('Set prompt', callback_data='set_prompt')
    btn3 = types.InlineKeyboardButton('Spend data', callback_data='spend_data')
    btn4 = types.InlineKeyboardButton('Ai', callback_data='ai')
    btn5 = types.InlineKeyboardButton('Clear', callback_data='clear')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'set_regex':
        bot.send_message(callback.message.chat.id, 'Set regex action')
    elif callback.data == 'set_prompt':
        states[callback.message.chat.id] = 'set_prompt'
        bot.send_message(callback.message.chat.id, 'Please enter the prompt:')
    elif callback.data == 'spend_data':
        bot.send_message(callback.message.chat.id, 'Spend data action')
    elif callback.data == 'ai':
        states[callback.message.chat.id] = 'ai'
    elif callback.data == 'clear':
        bot.send_message(callback.message.chat.id, 'Clear action')

@bot.message_handler(func=lambda message: states.get(message.chat.id) == 'set_prompt')
def handle_set_prompt(message):
    # Выводим сохраненное сообщение пользователя
    bot.send_message(message.chat.id, f'Your message: {message.text}')
    states[message.chat.id] = None

@bot.message_handler(func=lambda message: states.get(message.chat.id) == 'set_prompt')
def handle_set_ai(message):
    # Выводим сохраненное сообщение пользователя
    bot.send_message(message.chat.id, f'Your message: {message.text}')
    states[message.chat.id] = None


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.content_type == 'text':
        if message.text == 'Set regex':
            bot.send_message(message.chat.id, 'Set regex action')
        elif message.text == 'Set prompt':
            states[message.chat.id] = 'set_prompt'
            bot.send_message(message.chat.id, 'Please enter the prompt:')
        elif message.text == 'Spend data':
            bot.send_message(message.chat.id, 'Spend data action')
        elif message.text == 'ai':
            responses = run_ai()
            for response in responses:
                bot.send_message(message.chat.id, response)


def start_bot():
    bot.polling(none_stop=True)