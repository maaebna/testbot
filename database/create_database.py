import sqlite3


conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_text TEXT,
        message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()


def save_message_to_db(user_id, message_text):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_messages (user_id, message_text) VALUES (?, ?)", (user_id, message_text))
    conn.commit()
    conn.close()