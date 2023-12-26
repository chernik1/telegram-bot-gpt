with open('response.txt', 'r', encoding='utf-8') as file:
    text = file.read()

import re
pattern = r"\d{1,3}!(.+?)(?=\d|$)"
matches = re.findall(pattern, text)
for match in matches:
    print(match)