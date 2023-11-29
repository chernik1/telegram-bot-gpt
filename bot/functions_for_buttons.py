import os

from tools.ai.logic import run_ai



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

    for index, response in enumerate(responses, start=1):
        with open(rf'G:\telegram-bot-gpt\file\{index}', 'a+', encoding='utf-8') as file:
            file.write(f'{response}\n')
        #bot.send_message(message.chat.id, response, reply_markup=markup)