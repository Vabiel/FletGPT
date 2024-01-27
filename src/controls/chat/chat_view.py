import flet as ft

from src.app.gpt_model import GPTModel
from src.app.user_settings import UserSettings
from src.controls.chat.chat_item import ChatItem
from src.controls.chat.chat_list import ChatList
from src.app.di import DI
from src.app.events import Event
from src.app.gpt_core import GptCore
from src.models.message import Message
from src.models.user import User
from src.models.chat import Chat

MAX_LINES = 5
MIN_LINES = 1
HINT_TEXT = "Enter a promt here"


class ChatView(ft.Column):
    def __init__(self, border, radius, color):
        super().__init__()

        self.messages = []
        self.chat_id = None

        self.__setup_dependencies()
        self.__load_settings()
        self.__restore_chat()

        if self.chat_id is not None:
            self.__load_messages(self.chat_id)

        self.chat = ChatList([ChatItem(message) for message in self.messages])

        self.input_text = ft.TextField(
            on_submit=self.on_send_message,
            hint_text=HINT_TEXT,
            min_lines=MIN_LINES,
            max_lines=MAX_LINES,
            border_color=color,
            border_radius=radius,
            shift_enter=True,
            expand=True,
        )
        send_btn = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED, on_click=self.on_send_message, icon_color=color
        )
        self.controls = [
            ft.Container(
                content=self.chat,
                border=border,
                border_radius=radius,
                padding=radius,
                expand=True,
            ),
            ft.Row(
                [
                    self.input_text,
                    send_btn,
                ]
            ),
        ]

        self.expand = True

    def on_send_message(self, e):
        question = self.input_text.value
        if question != "":
            if self.chat_id is None:
                self.__create_new_chat()

            self.__create_user_message(question)

            gpt_message = Message.create(self.chat_id, self.gptUser, "")
            self.chat.controls.append(ChatItem(gpt_message))
            last_item = self.chat.controls[-1]
            self.input_text.read_only = True
            last_item.showLoader()
            msg = ""
            self.update()
            
            current_model = self.current_model
            
            try:
                response = GptCore.ask_question(self.__get_context(), current_model)
                for message in response:
                    msg += message
                    last_item.subtitle.value = msg
                    last_item.subtitle.update()
            except Exception as e:
                error_msg = f"an error occurred while executing the request: {e.args[0]}"
                print(error_msg)
                msg += f"\n{error_msg}"
                last_item.subtitle.value = msg
                last_item.subtitle.update()
            finally:
                gpt_message.message_text = msg
                last_item.message.message_text = msg
                last_item.hideLoader()
                self.input_text.read_only = False
                self.messages.append(gpt_message)
                self.messageProvider.create_message(gpt_message)
                self.update()

    def __create_new_chat(self):
        chat = Chat.create()
        self.chat_id = chat.chat_id
        self.chatProvider.create_chat(chat)
        self.storage.set(UserSettings.CURRENT_CHAT_ID, chat.chat_id)
        self.eventDispatcher.dispatch(Event.ON_ADD_CHAT, chat)
        
    def __create_user_message(self, text:str):
            user_message = Message.create(self.chat_id, self.user, text)
            self.chat.controls.append(ChatItem(user_message))

            self.input_text.value = ""
            self.messages.append(user_message)
            self.messageProvider.create_message(user_message)
            
    def __on_select_chat(self, data: Chat):
        chat_id = data.chat_id
        if chat_id != self.chat_id:
            self.chat_id = chat_id
            self.storage.set(UserSettings.CURRENT_CHAT_ID, chat_id)
            self.__load_messages(chat_id)
            self.__update_chat()

    def __lock_input(self):
        self.input_text.read_only = True
        
    def __unlock_input(self):
        self.input_text.read_only = False

    def __on_delete_chat(self, chat: Chat):
        chat_id = chat.chat_id
        if chat_id == self.chat_id:
            self.chat_id = None
            self.messages.clear()
            self.chat.clean()
            self.update()

    def __on_create_chat(self, chat: Chat):
        chat_id = chat.chat_id
        self.chat_id = chat_id
        self.chat.clean()
        self.update()

    def __on_change_settings(self, settings: tuple):
        self.current_model = settings[0]
        self.ignore_context_depth = settings[1]
        self.context_depth = settings[2]

    def __load_settings(self):
        storage = self.storage
        if storage.contains_key(UserSettings.CURRENT_MODEL):
            self.current_model = storage.get(UserSettings.CURRENT_MODEL)
        else:
            self.current_model = GPTModel.GPT_4
            storage.set(UserSettings.CURRENT_MODEL, self.current_model)

        if storage.contains_key(UserSettings.IGNORE_CONTEXT_DEPTH):
            self.ignore_context_depth = storage.get(UserSettings.IGNORE_CONTEXT_DEPTH)
        else:
            self.ignore_context_depth = False
            storage.set(UserSettings.IGNORE_CONTEXT_DEPTH, self.ignore_context_depth)
            
        if storage.contains_key(UserSettings.CONTEXT_DEPTH):
            self.context_depth = storage.get(UserSettings.CONTEXT_DEPTH)
        else:
            self.context_depth = 40
            storage.set(UserSettings.CONTEXT_DEPTH, self.context_depth)

    def __load_messages(self, chat_id: str):
        if self.messages:
            self.messages.clear()
        self.messages = self.messageProvider.read_messages_by_chat(chat_id)

    def __update_chat(self):
        self.chat.clean()
        for message in self.messages:
            self.chat.controls.append(ChatItem(message))
        self.update()

    def __get_context(self) -> list:
        ignore_context_depth = self.ignore_context_depth
        if not ignore_context_depth:
            depth = int(self.context_depth)
            messages = self.messages[-depth:] if len(self.messages) > depth else self.messages
        else:
            messages = self.messages
        
        return self.__create_context(messages)

    def __create_context(self, messages: list[Message]) -> list:
        return [
            {
                "role": "assistant" if message.is_gpt_message else "user",
                "content": message.message_text,
            }
            for message in messages
        ]

    def __setup_dependencies(self):
        di = DI.get_instance()
        self.userProvider = di.userProvider
        self.chatProvider = di.chatProvider
        self.messageProvider = di.messageProvider
        self.storage = di.storage
        self.eventDispatcher = di.eventDispatcher

        self.eventDispatcher.subscribe(
            event_name=Event.ON_SELECT_CHAT, handler=self.__on_select_chat
        )
        self.eventDispatcher.subscribe(
            event_name=Event.ON_DELETE_CHAT, handler=self.__on_delete_chat
        )
        self.eventDispatcher.subscribe(
            event_name=Event.ON_CREATE_CHAT, handler=self.__on_create_chat
        )
        self.eventDispatcher.subscribe(
            event_name=Event.ON_CHANGE_SETTINGS, handler=self.__on_change_settings
        )
        
    def __restore_chat(self):
        users = self.userProvider.get_default_users()
        self.user = users[User.DEFAULT_TYPE]
        self.gptUser = users[User.GPT_TYPE]

        if self.storage.contains_key(UserSettings.CURRENT_CHAT_ID):
            chat_id = self.storage.get(UserSettings.CURRENT_CHAT_ID)
            if self.chatProvider.is_exists(chat_id):
                self.chat_id = chat_id
            else:
                self.storage.remove(UserSettings.CURRENT_CHAT_ID)
