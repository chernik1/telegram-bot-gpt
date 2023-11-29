import dataclasses
from dataclasses import dataclass, field
import re
from collections import defaultdict
from typing import Any, Dict

@dataclasses.dataclass
class Config:
    symbols: str = '2000'
    regex: str = r'\d{1,2}\..+?(?=\n|$)'
    promt: str = ''
    tasks: str = ''
    promt_constant: str = 'Выполни запрос.'
    regex_promt: str = ''

    def __str__(self):
        return 'symbols: ' + self.symbols + '\n' + 'regex: ' + self.regex + '\n' + 'promt: ' + self.promt + '\n' + 'tasks: ' + self.tasks + '\n' + 'promt_constant: ' + self.promt_constant + '\n' + 'regex_promt: ' + self.regex_promt


@dataclasses.dataclass
class ConfigOneMessage(Config):
    promt: str = ''
    regex_tasks = ''
    regex_promt = ''

@dataclasses.dataclass
class ConfigConstructor(Config):
    pass

@dataclasses.dataclass
class Lesson:
     name: str
     short_name: str
     directory: str
     regex_dict: Dict[str, str]
     short_name_regex: str = r'\.\.[a-z]'
     symbols_promt: str = '2000'
     format_file: str = 'txt'






