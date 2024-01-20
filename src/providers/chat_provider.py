
# Создаем класс ChatProvider для работы с таблицей chats
from src.local_storage.db import DB
from src.models.chat import Chat


class ChatProvider:

  def __init__(self, db: DB):
    self.db = db

  # Метод create_chat для создания нового чата в таблице chats
  def create_chat(self, chat: Chat):
    sql = "INSERT INTO chats (chat_title, chat_date, chat_id) VALUES (?, ?, ?);"
    self.db.cursor.execute(sql, (chat.chat_title, chat.chat_date, chat.chat_id))
    self.db.conn.commit()

  # Метод read_chat для получения данных о чате по его идентификатору из таблицы chats
  def read_chat(self, chat_id: str):
    sql = "SELECT * FROM chats WHERE chat_id = ?;"
    self.db.cursor.execute(sql, (chat_id,))
    result = self.db.cursor.fetchone()
    if result:
      chat = Chat(*result)
    else:
      chat = None
    return chat

  # Метод read_chats для получения списка всех доступных чатов из таблицы chats
  def read_chats(self) -> list[Chat]:
    sql = "SELECT * FROM chats;"
    self.db.cursor.execute(sql)
    results = self.db.cursor.fetchall()
    chats = []
    for result in results:
        chat = Chat(*result)
        chats.append(chat)
    return chats

  # Метод update_chat для обновления данных о чате по его идентификатору в таблице chats
  def update_chat(self, chat: Chat):
    sql = "UPDATE chats SET chat_title = ?, chat_date = ? WHERE chat_id = ?;"
    self.db.cursor.execute(sql, (chat.chat_title, chat.chat_date, chat.chat_id))
    self.db.conn.commit()

  # Метод delete_chat для удаления чата по его идентификатору из таблицы chats
  def delete_chat(self, chat_id: str):
    sql = "DELETE FROM chats WHERE chat_id = ?;"
    self.db.cursor.execute(sql, (chat_id,))
    self.db.conn.commit()
