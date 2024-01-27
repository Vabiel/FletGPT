import sqlite3
from src.local_storage.db import DB
from src.models.user import User


class UserProvider:

  def __init__(self, db: DB):
    self.db = db
    self.db_file = self.db.db_file

  def create_user(self, user: User):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "INSERT INTO users (user_type, user_nickname, user_id) VALUES (?, ?, ?);"
    cursor.execute(sql, (user.user_type, user.user_nickname, user.user_id))
    conn.commit()
    conn.close()

  def get_user(self, user_id):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    if result:
      user = User(*result)
    else:
      user = None
    conn.close()
    return user

  def update_user(self, user: User):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "UPDATE users SET user_type = ?, user_nickname = ? WHERE user_id = ?;"
    cursor.execute(sql, (user.user_type, user.user_nickname, user.user_id))
    conn.commit()
    conn.close()

  def delete_user(self, user_id: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "DELETE FROM users WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()

  def get_users_by_type(self, user_type: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE user_type = ?;"
    cursor.execute(sql, (user_type,))
    results = cursor.fetchall()
    users = []
    for result in results:
      user = User(*result)
      users.append(user)
    conn.close()
    return users
  
  def get_user_by_type(self, user_type: str):
    conn = sqlite3.connect(self.db_file)
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE user_type = ? LIMIT 1;"
    cursor.execute(sql, (user_type,))
    result = cursor.fetchone()
    if result:
      user = User(*result)
    else:
      user = None
    conn.close()
    return user
  
  def get_default_users(self) -> dict:
    users = {}
    result = self.get_user_by_type(User.DEFAULT_TYPE)
    if result is not None:
      users[User.DEFAULT_TYPE] = result
    else:
      user = User.default("You")
      self.create_user(user)
      users[User.DEFAULT_TYPE] = user
      
    gpt_result = self.get_user_by_type(User.GPT_TYPE)
    if gpt_result is not None:
      users[User.GPT_TYPE] = gpt_result
    else:
      gpt = User.gpt("FletGPT")
      self.create_user(gpt)
      users[User.GPT_TYPE] = gpt 
    return users