from bot.telegram_interface import start_bot
import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect(r'db/database.db')

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS lessons(
        name_lesson TEXT PRIMARY KEY,
        id_question INTEGER,
        answer TEXT
    )""")

    conn.commit()

    conn.close()

    start_bot()




