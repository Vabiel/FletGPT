# Импортируем модуль sqlite3
import sqlite3

# Создаем класс DB для работы с базой данных
class DB:

  # Конструктор класса, принимает имя файла базы данных
  def __init__(self, db_file):
    # Создаем подключение к базе данных
    self.conn = sqlite3.connect(db_file)
    # Создаем курсор для выполнения SQL-запросов
    self.cursor = self.conn.cursor()
    # Вызываем метод initDB для создания таблиц, если их нет
    self.initDB()

  # Метод initDB для создания таблиц, если их нет
  def initDB(self):
    # Получаем список всех таблиц в базе данных
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = self.cursor.fetchall()

    # Проверяем, есть ли таблица чатов в списке
    if ('chats',) not in tables:
      # Если нет, то создаем ее
      self.cursor.execute("""
        CREATE TABLE chats (
          chat_id TEXT PRIMARY KEY, -- идентификатор чата
          chat_title TEXT NOT NULL, -- заголовок чата
          chat_date TEXT NOT NULL -- дата создания чата
        );
      """)

    # Проверяем, есть ли таблица пользователей в списке
    if ('users',) not in tables:
      # Если нет, то создаем ее
      self.cursor.execute("""
        CREATE TABLE users (
          user_id TEXT PRIMARY KEY, -- идентификатор пользователя
          user_type TEXT NOT NULL, -- тип пользователя
          user_nickname TEXT NOT NULL -- никнейм пользователя
        );
      """)

    # Проверяем, есть ли таблица сообщений в списке
    if ('messages',) not in tables:
      # Если нет, то создаем ее
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

    # Сохраняем изменения в базе данных
    self.conn.commit()

  # Деструктор класса, закрывает подключение к базе данных
  def __del__(self):
    # Закрываем подключение
    self.conn.close()

# Создаем объект класса DB, передавая имя файла базы данных
# db = DB("chat_app.db")
