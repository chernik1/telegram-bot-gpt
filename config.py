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
    prompt_constant: str = 'Выполни запрос.'
    regex_prompt: str = ''
    file_format = 'pdf'
    lesson = 'base'
    prompt = ''
    db_action_for_lesson: bool = False

    def __str__(self):
        return 'symbols: ' + self.symbols + '\n' + 'regex: ' + self.regex + '\n' + 'promt: ' + self.prompt + '\n' + 'tasks: ' + self.tasks + '\n' + 'promt_constant: ' + self.prompt_constant + '\n' + 'regex_promt: ' + self.regex_prompt



@dataclasses.dataclass
class Lesson:
     name: str
     short_name: str
     directory: str
     regex_dict: Dict[str, str]
     short_name_regex: str = r'\.\.[a-z]'
     symbols_promt: str = '2000'
     format_file: str = 'txt'






