import flet as ft

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
        
        
        di = DI.get_instance()
        self.eventDispatcher = di.eventDispatcher
        self.eventDispatcher.subscribe(event_name=Event.ON_SELECT_CHAT, handler=self.__on_select_chat)
        self.eventDispatcher.subscribe(event_name=Event.ON_DELETE_CHAT, handler=self.__on_delete_chat)
        self.eventDispatcher.subscribe(event_name=Event.ON_CREATE_CHAT, handler=self.__on_create_chat)
        self.userProvider = di.userProvider
        self.chatProvider = di.chatProvider
        self.messageProvider = di.messageProvider
        users = self.userProvider.get_default_users()
        self.user = users[User.DEFAULT_TYPE]
        self.gptUser = users[User.GPT_TYPE]
        self.storage = di.storage
        
        if self.storage.contains_key("current_chat_id"):
            self.chat_id = self.storage.get("current_chat_id")
        else:
            self.chat_id = None
            
        self.gpt = GptCore()
        
        controls = []
        
        if self.chat_id is not None:
           messages = self.messageProvider.read_messages_by_chat(self.chat_id)
           for message in messages:
               controls.append(ChatItem(message))
        
        self.chat = ChatList(controls)
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
                self.storage.set("current_chat_id", chat.chat_id)
                self.eventDispatcher.dispatch(Event.ON_ADD_CHAT, chat)
            
            userMessage = Message.create(self.chat_id, self.user, question)
            self.chat.controls.append(ChatItem(userMessage))

            self.input_text.value = ""
            self.input_text.read_only = True
            self.messageProvider.create_message(userMessage)
            self.update()

            gptMessage = Message.create(self.chat_id, self.gptUser, "")
            self.chat.controls.append(ChatItem(gptMessage))
            lastItem = self.chat.controls[-1]
            lastItem.showLoader()
            msg = ""
            self.update()
            response = self.gpt.ask_question(question=question)
            for message in response:
                msg+=message
                lastItem.subtitle.value=msg
                lastItem.subtitle.update()
            
            gptMessage.message_text = msg
            self.gpt.add_message(msg, is_assistant=True)
            lastItem.message.message_text=msg
            lastItem.hideLoader()
            self.input_text.read_only = False
            self.messageProvider.create_message(gptMessage)
            self.update()
    
    def __on_select_chat(self, data: Chat):
        chat_id = data.chat_id
        self.chat_id = chat_id
        self.storage.set("current_chat_id", chat_id)
        self.chat.clean()
        messages = self.messageProvider.read_messages_by_chat(self.chat_id)
        for message in messages:
            self.chat.controls.append(ChatItem(message))
        self.update()
        
    def __on_delete_chat(self, chat: Chat):
        chat_id = chat.chat_id
        if chat_id == self.chat_id:
            self.chat_id = None
            self.chat.clean()
            self.update()
            
    def __on_create_chat(self, chat: Chat):
        chat_id = chat.chat_id
        self.chat_id = chat_id
        self.chat.clean()
        self.update()
