# Создаем класс MessageProvider для работы с таблицей messages
from src.local_storage.db import DB
from src.models.message import Message


class MessageProvider:

  def __init__(self, db: DB):
    self.db = db

  # Метод create_message для создания нового сообщения в таблице messages
  def create_message(self, message: Message):
    sql = "INSERT INTO messages (chat_id, user_id, message_type, message_text, message_date) VALUES (?, ?, ?, ?, ?, ?);"
    self.db.cursor.execute(sql, (message.chat_id, message.user_id, message.message_type, message.message_text, message.message_date, message.message_id))
    self.db.conn.commit()

  # Метод read_message для получения данных о сообщении по его идентификатору из таблицы messages
  def read_message(self, message_id: str):
    sql = "SELECT * FROM messages WHERE message_id = ?;"
    self.db.cursor.execute(sql, (message_id,))
    result = self.db.cursor.fetchone()
    if result:
      message = Message(*result)
    else:
      message = None
    return message

  # Метод update_message для обновления данных о сообщении по его идентификатору в таблице messages
  def update_message(self, message: Message):
    sql = "UPDATE messages SET chat_id = ?, user_id = ?, message_type = ?, message_text = ?, message_date = ? WHERE message_id = ?;"
    self.db.cursor.execute(sql, (message.chat_id, message.user_id, message.message_type, message.message_text, message.message_date, message.message_id))
    self.db.conn.commit()

  # Метод delete_message для удаления сообщения по его идентификатору из таблицы messages
  def delete_message(self, message_id: str):
    sql = "DELETE FROM messages WHERE message_id = ?;"
    self.db.cursor.execute(sql, (message_id,))
    self.db.conn.commit()

  # Метод read_messages_by_chat для получения списка всех сообщений из определенного чата из таблицы messages
  def read_messages_by_chat(self, chat_id: str):
    sql = "SELECT * FROM messages WHERE chat_id = ?;"
    self.db.cursor.execute(sql, (chat_id,))
    results = self.db.cursor.fetchall()
    messages = []
    for result in results:
      message = Message(*result)
      messages.append(message)
    return messages
