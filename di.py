from src.local_storage.db import DB
from src.providers.chat_provider import ChatProvider
from src.providers.message_provider import MessageProvider
from src.providers.user_provider import UserProvider


class DI(object):
  def __init__(self):
      self.db = DB("flet_gpt_app.db")
      self.userProvider = UserProvider(self.db)
      self.chatProvider = ChatProvider(self.db)
      self.messageProvider = MessageProvider(self.db)
  
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(DI, cls).__new__(cls)
    return cls.instance

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    self.db.conn.close()

  @property
  def db(self) -> DB:
    return self._db

  @db.setter
  def db(self, value: DB):
    self._db = value

  @property
  def userProvider(self) -> UserProvider:
    return self._userProvider

  @userProvider.setter
  def userProvider(self, value: UserProvider):
    self._userProvider = value

  @property
  def chatProvider(self) -> ChatProvider:
    return self._chatProvider

  @chatProvider.setter
  def chatProvider(self, value: ChatProvider):
    self._chatProvider = value

  @property
  def messageProvider(self) -> MessageProvider:
    return self._messageProvider

  @messageProvider.setter
  def messageProvider(self, value: MessageProvider):
    self._messageProvider = value
