import flet as ft
from message import Message

class ChatItem(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        is_gpt_answer = message.is_gpt_answer 
        title = "FletGPT" if is_gpt_answer else "User"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Icon(ft.icons.ANDROID if is_gpt_answer else ft.icons.PERSON),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.INDIGO if is_gpt_answer else ft.colors.GREEN,
            ),
            ft.Column(
                [
                    ft.Text(title, weight="bold"),
                    ft.Text(message.text, selectable=True, width=500),
                ],
                spacing=1,
            ),
            
        ]