from docx import Document
import re
doc = Document('table.docx')

table = doc.tables[0]  # Первая таблица в документе

table_text = ""
for row in table.rows:
    for cell in row.cells:
        table_text += cell.text + "\t"
    table_text += "\n"

matches = re.findall(r'\$(.*?)\$', table_text)

# Вывод выделенного текста
for match in matches:
    if match == '' or match == ' ' or match == '\n':
        continue
    if len(match) < 6:
        continue
    print('$' + match.strip() + '$')