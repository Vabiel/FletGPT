import flet as ft
from chat_item import ChatItem
from chat_list import ChatList
from gpt_core import GptCore
from message import Message
from settings_dialog import SettingDialog
from sidebar import Sidebar


DEFAULT_COLOR = ft.colors.BLUE
DEFAULT_RADIUS = 8
DEFAULT_BORDER = ft.border.all(1, DEFAULT_COLOR)
MAX_LINES = 5
MIN_LINES = 1
HINT_TEXT = "Enter your message"


def main(page: ft.Page):
    page.title = "FletGPT"

    gpt = GptCore()
    
    preloader=ft.Container(bgcolor=ft.colors.BLACK,opacity=0.5, expand=True)

    def on_send_message(e):
        question = input_text.value
        if question != "":
            page.pubsub.send_all(Message(question, is_gpt_answer=False))

            input_text.value = ""
            input_text.focus()
            page.overlay.append(preloader)
            input_text.read_only = True
            page.update()

            answer = gpt.ask_question(question=question)
            page.pubsub.send_all(Message(answer, is_gpt_answer=True))

    def on_recieve_message(message: Message):
        chat.controls.append(ChatItem(message))
        if message.is_gpt_answer:
            page.overlay.clear()
            input_text.read_only = False
    
        page.update()

    chat = ChatList()

    input_text = ft.TextField(
        on_submit=on_send_message,
        hint_text=HINT_TEXT,
        min_lines=MIN_LINES,
        max_lines=MAX_LINES,
        border_color=DEFAULT_COLOR,
        border_radius=DEFAULT_RADIUS,
        shift_enter=True,
        expand=True,
    )
    
    send_btn = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED, on_click=on_send_message, icon_color=DEFAULT_COLOR
    )

    dialog = SettingDialog(page)

    page.pubsub.subscribe(on_recieve_message)

    page.add(
        ft.Row(
            [
                Sidebar(
                    border=DEFAULT_BORDER,
                    radius=DEFAULT_RADIUS,
                    bgcolor=DEFAULT_COLOR,
                    on_settings=dialog.show,
                ),
                ft.Column(
                    [
                        ft.Container(
                            content=chat,
                            border=DEFAULT_BORDER,
                            border_radius=DEFAULT_RADIUS,
                            padding=DEFAULT_RADIUS,
                            expand=True,
                        ),
                        ft.Row(
                            [
                                input_text,
                                send_btn,
                            ]
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        ),
    )


ft.app(target=main)
