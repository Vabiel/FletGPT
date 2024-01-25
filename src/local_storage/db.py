import sqlite3

class DB:

  def __init__(self, db_file):
    self.db_file = db_file
    
    self.initDB()

  def initDB(self):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if ('chats',) not in tables:
      cursor.execute("""
        CREATE TABLE chats (
          chat_id TEXT PRIMARY KEY,
          chat_title TEXT NOT NULL,
          chat_date TEXT NOT NULL
        );
      """)

    if ('users',) not in tables:
      cursor.execute("""
        CREATE TABLE users (
          user_id TEXT PRIMARY KEY,
          user_type TEXT NOT NULL,
          user_nickname TEXT NOT NULL
        );
      """)

    if ('messages',) not in tables:
      cursor.execute("""
        CREATE TABLE messages (
          message_id TEXT PRIMARY KEY,
          chat_id TEXT NOT NULL,
          user_id TEXT NOT NULL,
          message_type TEXT NOT NULL,
          message_text TEXT NOT NULL,
          message_date TEXT NOT NULL,
          FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE,
          FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        );
      """)

    if ('user_settings',) not in tables:
      cursor.execute("""
        CREATE TABLE user_settings (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL,
          type TEXT NOT NULL
        );
      """)
     
    conn.commit()
    conn.close()
    
