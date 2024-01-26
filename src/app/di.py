from src.app.event_dispatcher import EventDispatcher
from src.providers.user_settings_provider import UserSettingsProvider
from src.local_storage.db import DB
from src.providers.chat_provider import ChatProvider
from src.providers.message_provider import MessageProvider
from src.providers.user_provider import UserProvider
from flet_core.client_storage import ClientStorage


class DI(object):

  def __init__(self):
    self.db = DB("flet_gpt_app.db")
    self.userProvider = UserProvider(self.db)
    self.chatProvider = ChatProvider(self.db)
    self.messageProvider = MessageProvider(self.db)
    self.userSettingsProvider = UserSettingsProvider(self.db)
    self.eventDispatcher = EventDispatcher()
    self.__user_storage = None

  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(DI, cls).__new__(cls)
    return cls.instance

  @staticmethod
  def get_instance():
    if not hasattr(DI, 'instance'):
      DI.instance = DI()
    return DI.instance

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

  @property
  def userSettingsProvider(self) -> UserSettingsProvider:
    return self._userSettingsProvider

  @userSettingsProvider.setter
  def userSettingsProvider(self, value: UserSettingsProvider):
    self._userSettingsProvider = value
  
  @property
  def eventDispatcher(self) -> EventDispatcher:
    return self._eventDispatcher

  @eventDispatcher.setter
  def eventDispatcher(self, value: EventDispatcher):
    self._eventDispatcher = value
    
  def set_storage(self, storage: ClientStorage):
    if self.__user_storage is None:
      self.__user_storage = storage

  @property
  def storage(self) -> ClientStorage | None :
    if self.__user_storage is not None:
      return self.__user_storage
    else:
      return None