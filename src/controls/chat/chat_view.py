import flet as ft

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

        self.gpt = GptCore()
        self.messages = []
        self.chat_id = None

        self.__setup_dependencies()
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
                chat = Chat.create()
                self.chat_id = chat.chat_id
                self.chatProvider.create_chat(chat)
                self.storage.set(UserSettings.CURRENT_CHAT_ID, chat.chat_id)
                self.eventDispatcher.dispatch(Event.ON_ADD_CHAT, chat)

            userMessage = Message.create(self.chat_id, self.user, question)
            self.chat.controls.append(ChatItem(userMessage))

            self.input_text.value = ""
            self.input_text.read_only = True
            self.messages.append(userMessage)
            self.messageProvider.create_message(userMessage)
            self.update()

            gptMessage = Message.create(self.chat_id, self.gptUser, "")
            self.chat.controls.append(ChatItem(gptMessage))
            lastItem = self.chat.controls[-1]
            lastItem.showLoader()
            msg = ""
            self.update()
            
            response = self.gpt.ask_question(self.__get_context())
            for message in response:
                msg += message
                lastItem.subtitle.value = msg
                lastItem.subtitle.update()

            gptMessage.message_text = msg
            lastItem.message.message_text = msg
            lastItem.hideLoader()
            self.input_text.read_only = False
            self.messages.append(gptMessage)
            self.messageProvider.create_message(gptMessage)
            self.update()

    def __on_select_chat(self, data: Chat):
        chat_id = data.chat_id
        if chat_id != self.chat_id:
            self.chat_id = chat_id
            self.storage.set(UserSettings.CURRENT_CHAT_ID, chat_id)
            self.__load_messages(chat_id)
            self.__update_chat()

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

    def __load_messages(self, chat_id: str):
        if self.messages:
            self.messages.clear()
        self.messages = self.messageProvider.read_messages_by_chat(chat_id)

    def __update_chat(self):
        self.chat.clean()
        for message in self.messages:
            self.chat.controls.append(ChatItem(message))
        self.update()

    def __get_context(self, depth: int = 40) -> list:
        messages = self.messages[-depth:] if len(self.messages) > depth else self.messages
        
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

    def __restore_chat(self):
        users = self.userProvider.get_default_users()
        self.user = users[User.DEFAULT_TYPE]
        self.gptUser = users[User.GPT_TYPE]

        if self.storage.contains_key(UserSettings.CURRENT_CHAT_ID):
            self.chat_id = self.storage.get(UserSettings.CURRENT_CHAT_ID)
