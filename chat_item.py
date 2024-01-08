import flet as ft
import pyperclip
from message import Message

class ChatItem(ft.ListTile):
    def __init__(self, message: Message):
        super().__init__()
        is_gpt_answer = message.is_gpt_answer 
        title = "FletGPT" if is_gpt_answer else "User"
        self.leading=ft.CircleAvatar(
                            content=ft.Icon(ft.icons.ANDROID if is_gpt_answer else ft.icons.PERSON),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.INDIGO if is_gpt_answer else ft.colors.GREEN,
                        )
        self.title=ft.Text(title, weight="bold")
        self.subtitle=ft.Text(message.text, selectable=True)
        self.content_padding=ft.padding.all(0.0)
        self.dense=True
        self.is_three_line=True
        
        def copy_text(_):
            pyperclip.copy(message.text)
        
        if (is_gpt_answer):
            self.trailing=ft.IconButton(
                            on_click=copy_text,
                            icon=ft.icons.COPY,
                            icon_color=ft.colors.GREEN,
                            icon_size=16,       
                        )
