from docx import Document
import sqlite3
from docx.shared import Pt

def form_info() -> dict:
    name_multitask = input('Введите название мультитаски\n')
    info = {}

    db = sqlite3.connect(r'db/database.db')
    cur = db.cursor()

    for answer_id in range(1, 102):
        cur.execute(
            f"""SELECT question, answer FROM multitask WHERE name_multitask = ' {name_multitask + "_" + str(answer_id)}'""")
        result = cur.fetchone()
        question = result[0] if result else None
        answer = result[1] if result else None
        info[question] = answer

    db.close()

    return info

def form_table(info) -> Document:
    doc = Document()
    table = doc.add_table(rows=1, cols=2)
    table.cell(0, 0).text = 'Вопрос'
    table.cell(0, 1).text = 'Ответ'


    for key, value in info.items():
        row = table.add_row()
        row.cells[0].text = key
        row.cells[1].text = value

    font_size = Pt(8)
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = font_size

    table.columns[1].width = Pt(40)

    doc.save('table.docx')

info = form_info()
form_table(info)

