import uuid

# Создаем класс User для представления данных о пользователе
class User:
  __DEFAULT_TYPE = "Default"
  __GPT_TYPE = "GPT"
  
  # Конструктор класса, принимает идентификатор, тип и никнейм пользователя
  def __init__(self, user_id: str, user_type: str, user_nickname: str):
    # Сохраняем атрибуты в объекте класса
    self.user_id = user_id
    self.user_type = user_type
    self.user_nickname = user_nickname

  # Метод __str__ для возвращения строкового представления объекта класса
  def __str__(self):
    # Формируем строку с данными о пользователе
    return f"User {self.user_id}: {self.user_type} {self.user_nickname}"

  @staticmethod
  def default(user_nickname: str):
    uid = uuid.uuid4()
    return User(str(uid), User.__DEFAULT_TYPE, user_nickname)

  @staticmethod
  def gpt(user_nickname: str):
    uid = uuid.uuid4()  
    return User(str(uid), User.__GPT_TYPE, user_nickname)

  @property
  def is_default(self):
    return self.user_type == User.__DEFAULT_TYPE

  @property
  def is_gpt(self):
    return self.user_type == User.__GPT_TYPE