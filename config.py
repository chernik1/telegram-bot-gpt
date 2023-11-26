import dataclasses
from dataclasses import dataclass
import re
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