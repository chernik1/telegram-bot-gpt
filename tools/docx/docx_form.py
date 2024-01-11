from docx import Document
import sqlite3

doc = Document()
name_multitask = input('Введите название мультитаски\n')

db = sqlite3.connect(r'db/database.db')
cur = db.cursor()

for answer_id in range(1, 102):
    cur.execute(
        f"""SELECT question, answer FROM multitask WHERE name_multitask = ' {name_multitask + "_" + str(answer_id)}'""")
    result = cur.fetchone()
    question = result[0] if result else None
    answer = result[1] if result else None
    print(question, answer)
db.close()

