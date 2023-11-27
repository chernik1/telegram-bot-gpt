import g4f
import re
import asyncio
import time
from threading import Thread
from queue import Queue
from config import Config

async def make_promt(promt):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": promt}],
        )
    except Exception as e:
        print(e)
        response = ['None']
    return response

async def create_tasks(promt_list):
    tasks = []
    for index, promt in enumerate(promt_list):

        task = asyncio.create_task(make_promt(promt))
        tasks.append(task)

    return tasks

async def validate_response(response):
    regex_link_begin = r'\[\d+\]:\s*".*?"' # ссылки в скобках
    regex_link_end = r'\bhttps?://\S+\b' # конечные ссылки
    regex_after_link = r'\[\d+\]:\s*(?:/\s*)?".*?"' # скобки
    regex_bing = r'Здравствуйте, это Bing\..*?.' #привествия бинга

    new_reponse = re.sub(regex_link_begin, '', response)
    new_reponse = re.sub(regex_link_end, '', new_reponse)
    new_reponse = re.sub(regex_after_link, '', new_reponse)
    new_reponse = re.sub(regex_bing, '', new_reponse)

    return new_reponse.strip()


async def start_ai(config: Config):
    #promt_user = re.match(r'...+', promt_all, re.DOTALL)
    # with open(r'G:\telegram-bot-gpt\ai\question.txt', 'r', encoding='utf-8') as file:
    #     question = file.read()
    #     regex = re.compile(r'\d.+')
    #     split_promt = re.findall(regex, question)
    #     if len(split_promt) == 0:
    #         raise SyntaxError('Ничего не нашлось под регулярное выражение')

    promt = config.promt.strip()
    symbols = config.symbols.strip()
    regex = config.regex.strip()
    promt = config.promt.strip()
    tasks = config.tasks.strip()
    promt_constant = config.promt_constant.strip()

    if promt == '' and tasks != '' and promt_constant != '' and regex != '':


        split_promt = re.findall(regex, tasks, re.DOTALL | re.I)

        promt_list = [promt + ' ' + promt_constant + ' ' + f' Лимит символов не должен превышать {symbols}' for promt in split_promt]

        all_repsonse = []

        tasks = await create_tasks(promt_list)
        print(tasks)

        responses = await asyncio.gather(*tasks)

        responses = [await validate_response(response) for response in responses]

        status = True

        return (responses, status)
    elif promt != '':
        # 1. task \n 2. task \n .... .. promt
        # regex_for_task = config.regex.strip()
        # regex_for_promt = r'.. +'
        #
        # promt = re.findall(regex_for_promt, promt, re.DOTALL)[0]
        # tasks = re.findall(regex_for_task, tasks, re.DOTALL)
        # symbols = config.symbols.strip()
        #
        # promt_list = [task + ' ' + promt + ' ' + f' Лимит символов не должен превышать {symbols}' for task in tasks]
        #
        # tasks = await create_tasks(promt_list)
        #
        # responses = await asyncio.gather(*tasks)
        #
        # responses = [await validate_response(response) for response in responses]
        #
        # status = True
        #
        # return (responses, status)
        promt = config.promt
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": promt}],
        )
        return response
    else:
        status = False
        return (None, status)

def run_ai(promt_user=None):
    time_start = time.time()
    result_queue = Queue()
    print(time_start)
    def run_async_code():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_ai(promt_user))
        loop.close()
        result_queue.put(result)

    thread = Thread(target=run_async_code)
    thread.start()
    thread.join()

    result = result_queue.get()

    print(time.time() - time_start)

    return result