import uuid
import datetime

# Создаем класс Chat для представления данных о чате
class Chat:

  def __init__(self, chat_id: str, chat_title: str, chat_date: str):
    self.chat_id = chat_id
    self.chat_title = chat_title
    self.chat_date = chat_date

  def __str__(self):
    return f"Chat {self.chat_id}: {self.chat_title} ({self.chat_date})"

  @staticmethod
  def create(chat_title: str):
    uid = uuid.uuid4()
    current_datetime = datetime.datetime.now()
    datetime_str = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    return Chat(str(uid), chat_title, datetime_str)
