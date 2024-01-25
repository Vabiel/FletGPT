import flet as ft
import pyperclip

from src.models.message import Message


class ChatItem(ft.ListTile):
    def __init__(self, message: Message):
        super().__init__()
        self.message = message
        is_gpt_answer = message.is_gpt_message
        title = "FletGPT" if is_gpt_answer else "You"
        self.indicator = ft.ProgressRing(width=40, height=40, visible=False)
        self.leading = ft.CircleAvatar(
            content=ft.Stack(
                [
                    self.indicator,
                    ft.Container(
                        content=ft.Icon(
                            ft.icons.ANDROID if is_gpt_answer else ft.icons.PERSON,
                            size=32,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ],
                width=40,
                height=40,
            ),
            color=ft.colors.WHITE,
            bgcolor=ft.colors.INDIGO if is_gpt_answer else ft.colors.GREEN,
        )
        self.title = ft.Text(title, weight="bold")
        self.subtitle = ft.Markdown(
            self.message.message_text,
            selectable=True,
            extension_set="gitHubFlavored",
            code_theme="atom-one-dark",
            code_style=ft.TextStyle(font_family="Roboto Mono"),
            on_tap_link=lambda e: print(e.data),
        )
        self.content_padding = ft.padding.all(0.0)
        self.dense = True
        self.is_three_line = True

        def copy_text(e):
            pyperclip.copy(self.message.message_text)

        if is_gpt_answer:
            self.trailing = ft.IconButton(
                on_click=copy_text,
                icon=ft.icons.COPY,
                icon_color=ft.colors.GREEN,
                icon_size=16,
            )

    def showLoader(self):
        self.indicator.visible = True

    def hideLoader(self):
        self.indicator.visible = False
