import flet as ft

from src.app.user_settings import UserSettings
from src.app.events import Event
from src.controls.history.history_item import HistoryItem
from src.app.di import DI
from src.models.chat import Chat


class HistoryList(ft.Container):
    def __init__(self, border, bgcolor, radius, on_settings):
        super().__init__()
        di = DI.get_instance()
        self.storage = di.storage
        if self.storage.contains_key("current_chat_id"):
            self.current_chat_id = self.storage.get("current_chat_id")
        else:
            self.current_chat_id = None
        self.eventDispatcher = di.eventDispatcher
        self.chatProvider = di.chatProvider
        self.eventDispatcher.subscribe(event_name=Event.ON_ADD_CHAT, handler=self.__on_add_chat)
        self.list = ft.ListView(expand=True, auto_scroll=False, spacing=0)
        self.chats = []
        self.__load_chats()
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Chats history"),
                        ft.TextButton(
                            "New chat",
                            icon=ft.icons.ADD,
                            on_click=self.__on_create_chat,
                        ),
                    ]
                ),
                ft.Divider(color=bgcolor, height=1),
                self.list,
                ft.Divider(color=bgcolor, height=1),
                ft.TextButton("Settings", icon=ft.icons.SETTINGS, on_click=on_settings),
            ],
            expand=True,
        )
        self.padding = ft.padding.all(15)
        self.margin = ft.margin.all(0)
        self.width = 250
        self.border = border
        self.border_radius = radius

    def __load_chats(self):
        self.chats.clear()
        self.chats = self.chatProvider.read_chats()
        self.__refresh_list()
    
    def __refresh_list(self):
        self.list.controls.clear()
        for chat in self.chats:
            self.list.controls.append(HistoryItem(chat, self.__on_rename, self.__on_delete, self.__on_select, selected=chat.chat_id == self.current_chat_id))
        
        
    
    def __on_create_chat(self, e):

        count = len(self.chats)+1
        chat = Chat.create(f"New chat {count}")
        chat_id = chat.chat_id
        self.current_chat_id = chat_id
        self.chatProvider.create_chat(chat)
        self.chats.insert(0,chat)
        self.storage.set("current_chat_id", chat_id)
        self.eventDispatcher.dispatch(event_name=Event.ON_CREATE_CHAT, data=chat)
        self.__refresh_list()
        self.update()
        
    def __on_add_chat(self, chat:Chat):
        if chat not in self.chats:
            self.current_chat_id = chat.chat_id
            self.chats.insert(0,chat)
            self.__refresh_list()
            self.update()
        
    def __on_rename(self, chat:Chat):
        print(chat.chat_id)
        print(chat.chat_title)
        print(chat.chat_date)
    
    def __on_delete(self, chat:Chat):
        chat_id = chat.chat_id
        self.chatProvider.delete_chat(chat_id)
        self.__load_chats()
        if self.current_chat_id == chat_id:
            self.current_chat_id = None
            self.current_chat_id = self.storage.remove(UserSettings.CURRENT_CHAT_ID)
            
        self.eventDispatcher.dispatch(event_name=Event.ON_DELETE_CHAT, data=chat)
        self.update()
    
    def __on_select(self, chat:Chat):
        chat_id = chat.chat_id
        if self.current_chat_id != chat_id:
            self.current_chat_id = chat_id
            self.eventDispatcher.dispatch(event_name=Event.ON_SELECT_CHAT, data=chat)
            self.__refresh_list()
            self.update()
