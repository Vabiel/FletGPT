import sqlite3
from src.local_storage.db import DB
from src.models.message import Message


class MessageProvider:

  def __init__(self, db: DB):
    self.db = db
    self.db_file = self.db.db_file

  def create_message(self, message: Message):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "INSERT INTO messages (chat_id, user_id, message_type, message_text, message_date, message_id) VALUES (?, ?, ?, ?, ?, ?);"
    cursor.execute(sql, (message.chat_id, message.user_id, message.message_type, message.message_text, message.message_date, message.message_id))
    conn.commit()
    conn.close()

  def read_message(self, message_id: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM messages WHERE message_id = ?;"
    cursor.execute(sql, (message_id,))
    result = self.db.cursor.fetchone()
    if result:
      message = Message(*result)
    else:
      message = None
    conn.close()
    return message

  def update_message(self, message: Message):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "UPDATE messages SET chat_id = ?, user_id = ?, message_type = ?, message_text = ?, message_date = ? WHERE message_id = ?;"
    cursor.execute(sql, (message.chat_id, message.user_id, message.message_type, message.message_text, message.message_date, message.message_id))
    conn.commit()
    conn.close()

  def delete_message(self, message_id: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "DELETE FROM messages WHERE message_id = ?;"
    cursor.execute(sql, (message_id,))
    conn.commit()
    conn.close()

  def read_messages_by_chat(self, chat_id: str) -> list[Message]:
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM messages WHERE chat_id = ?;"
    cursor.execute(sql, (chat_id,))
    results = cursor.fetchall()
    messages = []
    for result in results:
      message = Message(*result)
      messages.append(message)
    conn.close()
    return messages
