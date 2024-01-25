import uuid
import datetime

from src.models.chat import Chat
from src.models.user import User

class Message:
  __USER_MESSAGE = "user_message_type"
  __GPT_MESSAGE = "gpt_message_type"
  
  def __init__(self, message_id: str, chat_id: str, user_id: str, message_type: str, message_text: str, message_date: str):
    self.message_id = message_id
    self.chat_id = chat_id
    self.user_id = user_id
    self.message_type = message_type
    self.message_text = message_text
    self.message_date = message_date

  def __str__(self):
    return f"Message {self.message_id}: {self.message_type} {self.message_text} from user {self.user_id} in chat {self.chat_id} on {self.message_date}"

  @staticmethod
  def create(chat_id: str, user: User, message_text: str):
    uid = uuid.uuid4()
    current_datetime = datetime.datetime.now()
    datetime_str = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    message_type = Message.__GPT_MESSAGE if user.is_gpt else Message.__USER_MESSAGE
    return Message(str(uid), chat_id, user.user_id, message_type, message_text, datetime_str)

  @property
  def is_user_message(self):
    return self.message_type == Message.__USER_MESSAGE

  @property
  def is_gpt_message(self):
    return self.message_type == Message.__GPT_MESSAGE
