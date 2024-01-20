import sqlite3

class DB:

  def __init__(self, db_file):
    self.conn = sqlite3.connect(db_file)
    self.cursor = self.conn.cursor()
    self.initDB()

  def initDB(self):
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = self.cursor.fetchall()

    if ('chats',) not in tables:
      self.cursor.execute("""
        CREATE TABLE chats (
          chat_id TEXT PRIMARY KEY, -- идентификатор чата
          chat_title TEXT NOT NULL, -- заголовок чата
          chat_date TEXT NOT NULL -- дата создания чата
        );
      """)

    if ('users',) not in tables:
      self.cursor.execute("""
        CREATE TABLE users (
          user_id TEXT PRIMARY KEY, -- идентификатор пользователя
          user_type TEXT NOT NULL, -- тип пользователя
          user_nickname TEXT NOT NULL -- никнейм пользователя
        );
      """)

    if ('messages',) not in tables:
      self.cursor.execute("""
        CREATE TABLE messages (
          message_id TEXT PRIMARY KEY, -- идентификатор сообщения
          chat_id TEXT NOT NULL, -- идентификатор чата
          user_id TEXT NOT NULL, -- идентификатор пользователя
          message_type TEXT NOT NULL, -- тип сообщения
          message_text TEXT NOT NULL, -- текст сообщения
          message_date TEXT NOT NULL, -- дата сообщения
          FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE, -- при удалении чата удаляются все сообщения связанные с ним
          FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- при удалении пользователя удаляются все чаты и сообщения связанные с ним
        );
      """)

    self.conn.commit()
