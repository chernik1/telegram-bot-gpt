import dataclasses
from dataclasses import dataclass, field
import re
from collections import defaultdict
from typing import Any, Dict

@dataclasses.dataclass
class Config:
    symbols: str = '5000'
    regex: str = r'(?:\d{1,3}\..+?)(?=\d{1,3}\.|$)'
    tasks: str = ''
    prompt_constant: str = 'Выполни задачу.'
    regex_prompt: str = ''
    prompt = ''
    name_multitask = 'base'
    db_action_for_pack: bool = False

    def __str__(self):
        return 'symbols: ' + self.symbols + '\n' + 'regex: ' + self.regex + '\n' + 'promt: ' + self.prompt + '\n' + 'tasks: ' + self.tasks + '\n' + 'promt_constant: ' + self.prompt_constant + '\n' + 'regex_promt: ' + self.regex_prompt