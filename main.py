from bot.telegram_interface import start_bot
import sqlite3


if __name__ == '__main__':
    # conn = sqlite3.connect(r'db/database.db')
    #
    # cur = conn.cursor()
    #
    # cur.execute("""CREATE TABLE IF NOT EXISTS users(
    #    userid INT PRIMARY KEY,
    #    fname TEXT,
    #    lname TEXT,
    #    gender TEXT);
    # """)
    # conn.commit()


    start_bot()




