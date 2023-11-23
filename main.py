import g4f
import re
import asyncio
import time

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

async def main():
    with open('question.txt', 'r', encoding='utf-8') as file:
        question = file.read()
        regex = re.compile(r'\d.+')
        split_promt = re.findall(regex, question)
        if len(split_promt) == 0:
            raise SyntaxError('Ничего не нашлось под регулярное выражение')

    base_sub = ' Реши задание. По формулам. Мне нужно будет скопировать твой текст, поэтому отвечай только кодировкой utf-8 не нужно использовать Markdown или Latex'
    promt_list = [promt + base_sub for promt in split_promt]

    all_repsonse = []

    tasks = await create_tasks(promt_list)

    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.replace('\n', ''))





if __name__ == '__main__':
    time_start = time.time()
    asyncio.run(main())
    time_end = time.time()

    print(time_end - time_start)





