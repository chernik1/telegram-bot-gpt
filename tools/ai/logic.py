import g4f
import re
import asyncio
import time
from threading import Thread
from queue import Queue
from config import Config

async def make_prompt(prompt: str) -> str:
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print(prompt)
        response = ['None']
    return response

async def create_tasks(prompt_list: list) -> list:
    tasks = []
    for index, prompt in enumerate(prompt_list):

        task = asyncio.create_task(make_prompt(prompt))
        tasks.append(task)

    return tasks

async def validate_response(response: str) -> str:
    try:
        regex_link_begin = r'\[\d+\]:\s*".*?"' # ссылки в скобках
        regex_link_end = r'\bhttps?://\S+\b' # конечные ссылки
        regex_after_link = r'\[\d+\]:\s*(?:/\s*)?".*?"' # скобки
        regex_bing = r'Здравствуйте, это Bing\..*?.' #привествия бинга

        new_reponse = re.sub(regex_link_begin, '', response)
        new_reponse = re.sub(regex_link_end, '', new_reponse)
        new_reponse = re.sub(regex_after_link, '', new_reponse)
        new_reponse = re.sub(regex_bing, '', new_reponse)

        return new_reponse.strip()
    except:
        return 'Неудача'


async def start_ai(config: Config) -> tuple:
    prompt = config.prompt
    symbols = config.symbols.strip()
    regex = config.regex.strip()
    tasks = config.tasks.strip()
    prompt_constant = config.prompt_constant.strip()

    if prompt == '' and tasks != '' and prompt_constant != '' and regex != '':


        split_prompt = re.findall(regex, tasks, re.DOTALL | re.I)

        prompt_list = [prompt + ' ' + prompt_constant + ' ' + f' Лимит символов не должен превышать {symbols}' for prompt in split_prompt]

        all_repsonse = []

        split_tasks_10 = [prompt_list[i:i + 10] for i in range(0, len(prompt_list), 10)]

        for count, prompt_list in enumerate(split_tasks_10, 1):
            print(f'{count} / {len(split_tasks_10)}')
            tasks = await create_tasks(prompt_list)

            responses = await asyncio.gather(*tasks)

            responses = [await validate_response(response) for response in responses]

            all_repsonse += responses

        status = True

        return (all_repsonse, status, split_prompt)
    elif prompt != '':
        prompt = config.prompt
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    else:
        status = False
        return (None, status)

def run_ai(prompt_user=None) -> tuple:
    time_start = time.time()
    result_queue = Queue()
    print(time_start)
    def run_async_code():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_ai(prompt_user))
        loop.close()
        result_queue.put(result)

    thread = Thread(target=run_async_code)
    thread.start()
    thread.join()

    result = result_queue.get()

    print(time.time() - time_start)

    return result