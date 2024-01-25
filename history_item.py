
import flet as ft

from src.models.chat import Chat

class HistoryItem(ft.ListTile):
    def __init__(self, chat: Chat, on_rename, on_delete, on_select, selected: bool = True):
        super().__init__(
            selected=selected,
            title=ft.Text(chat.chat_title),
            trailing=ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(text="Rename chat", on_click=lambda _: on_rename(chat)),
                    ft.PopupMenuItem(text="Delete chat", on_click=lambda _: on_delete(chat)),
                ],
            ),
            height=40,
            content_padding=ft.padding.all(0),
            data=chat.chat_id,
            on_click=lambda _: on_select(chat),
        )

