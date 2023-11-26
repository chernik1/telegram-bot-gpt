import g4f
import re
import asyncio
import time
from threading import Thread
from queue import Queue

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

async def start_ai(promt_user=None):
    with open(r'G:\telegram-bot-gpt\ai\question.txt', 'r', encoding='utf-8') as file:
        question = file.read()
        regex = re.compile(r'\d.+')
        split_promt = re.findall(regex, question)
        if len(split_promt) == 0:
            raise SyntaxError('Ничего не нашлось под регулярное выражение')

    base_sub = ' Реши задание. По формулам. Мне нужно будет скопировать твой текст, поэтому отвечай только кодировкой utf-8 не нужно использовать Markdown или Latex'
    promt_list = [promt + promt_user for promt in split_promt]

    all_repsonse = []

    tasks = await create_tasks(promt_list)
    print(tasks)

    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.replace('\n', ''))

    return responses

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