# Создаем класс UserProvider для работы с таблицей users
from src.local_storage.db import DB
from src.models.user import User


class UserProvider:

  def __init__(self, db: DB):
    self.db = db

  # Метод create_user для создания нового пользователя в таблице users
  def create_user(self, user: User):
    sql = "INSERT INTO users (user_type, user_nickname) VALUES (?, ?, ?);"
    self.db.cursor.execute(sql, (user.user_type, user.user_nickname, user.user_id))
    self.db.conn.commit()

  # Метод read_user для получения данных о пользователе по его идентификатору из таблицы users
  def read_user(self, user_id):
    sql = "SELECT * FROM users WHERE user_id = ?;"
    self.db.cursor.execute(sql, (user_id,))
    result = self.db.cursor.fetchone()
    if result:
      user = User(*result)
    else:
      user = None
    return user

  # Метод update_user для обновления данных о пользователе по его идентификатору в таблице users
  def update_user(self, user: User):
    sql = "UPDATE users SET user_type = ?, user_nickname = ? WHERE user_id = ?;"
    self.db.cursor.execute(sql, (user.user_type, user.user_nickname, user.user_id))
    self.db.conn.commit()

  # Метод delete_user для удаления пользователя по его идентификатору из таблицы users
  def delete_user(self, user_id: str):
    sql = "DELETE FROM users WHERE user_id = ?;"
    self.db.cursor.execute(sql, (user_id,))
    self.db.conn.commit()

  # Метод read_users_by_type для получения списка всех пользователей определенного типа из таблицы users
  def read_users_by_type(self, user_type: str):
    sql = "SELECT * FROM users WHERE user_type = ?;"
    self.db.cursor.execute(sql, (user_type,))
    results = self.db.cursor.fetchall()
    users = []
    for result in results:
      user = User(*result)
      users.append(user)
    return users
