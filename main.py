from bot.telegram_interface import start_bot
import sqlite3


if __name__ == '__main__':
    # conn = sqlite3.connect(r'db/database.db')
    #
    # cur = conn.cursor()
    #
    # cur.execute("""CREATE TABLE IF NOT EXISTS lessons(
    #    lesson_id INT PRIMARY KEY,
    #    name TEXT,
    #    short_name TEXT,
    #    directory TEXT);
    # """)
    # conn.commit()


    start_bot()




