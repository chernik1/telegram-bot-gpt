from tools.ai.logic import run_ai
from config import Config
import pytest


def form_config() -> Config:
    with open('tests/tests_for_ai/files/tasks_prompt_constant.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()

    index_split = text.index('***\n')
    tasks = text[:index_split]
    promt_constant = text[index_split + 1:]

    config = Config()
    config.tasks = ''.join(tasks)
    config.promt_constant = ''.join(promt_constant)

    return config

def test_tasks_and_promt_constant():
    config = form_config()

    responses_status = run_ai(config)

    assert responses_status[1] == True