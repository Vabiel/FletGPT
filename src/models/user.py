import uuid

class User:
  __DEFAULT_TYPE = "Default"
  __GPT_TYPE = "GPT"
  
  def __init__(self, user_id: str, user_type: str, user_nickname: str):
    self.user_id = user_id
    self.user_type = user_type
    self.user_nickname = user_nickname

  def __str__(self):
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