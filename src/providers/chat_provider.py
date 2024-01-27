
import sqlite3
from src.local_storage.db import DB
from src.models.chat import Chat


class ChatProvider:

  def __init__(self, db: DB):
    self.db = db
    self.db_file = self.db.db_file

  def create_chat(self, chat: Chat):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "INSERT INTO chats (chat_title, chat_date, chat_id) VALUES (?, ?, ?);"
    cursor.execute(sql, (chat.chat_title, chat.chat_date, chat.chat_id))
    conn.commit()
    conn.close()

  def read_chat(self, chat_id: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM chats WHERE chat_id = ?;"
    cursor.execute(sql, (chat_id,))
    result = cursor.fetchone()
    if result:
      chat = Chat(*result)
    else:
      chat = None
    conn.close()
    return chat

  def read_chats(self) -> list[Chat]:
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM chats ORDER BY chat_date DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    chats = []
    for result in results:
        chat = Chat(*result)
        chats.append(chat)
    conn.close()
    return chats

  def update_chat(self, chat: Chat):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "UPDATE chats SET chat_title = ?, chat_date = ? WHERE chat_id = ?;"
    cursor.execute(sql, (chat.chat_title, chat.chat_date, chat.chat_id))
    conn.commit()
    conn.close()

  def delete_chat(self, chat_id: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "DELETE FROM chats WHERE chat_id = ?;"
    cursor.execute(sql, (chat_id,))
    cascade_sql = "DELETE FROM messages WHERE chat_id = ?;"
    cursor.execute(cascade_sql, (chat_id,))
    conn.commit()
    conn.close()
