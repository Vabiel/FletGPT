import flet as ft
from chat_item import ChatItem
from chat_list import ChatList
from gpt_core import GptCore
from message import Message

DEFAULT_COLOR = ft.colors.BLUE
DEFAULT_RADIUS = 8
DEFAULT_BORDER = ft.border.all(1, DEFAULT_COLOR)
MAX_LINES = 5
MIN_LINES = 1
HINT_TEXT="Enter your message"

def main(page: ft.Page):
    page.title = "FletGPT"
    
    gpt = GptCore()

    def on_send_message(_):
        question = input_text.value
        if question != "":
            page.pubsub.send_all(Message(question, is_gpt_answer=False))
            
            input_text.value = ""
            input_text.focus()
            preloader.visible=True
            input_text.read_only=True
            input_text.opacity=0.5
            send_btn.disabled=True
            send_btn.opacity=0.5
            page.update()
            
            answer = gpt.ask_question(question=question)
            page.pubsub.send_all(Message(answer, is_gpt_answer=True))
        

    def on_recieve_message(message: Message):
        chat.controls.append(ChatItem(message))
        if message.is_gpt_answer:
            preloader.visible=False
            input_text.read_only=False
            input_text.opacity=1.0
            send_btn.disabled=False
            send_btn.opacity=1.0
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
        icon=ft.icons.SEND_ROUNDED,
        on_click=on_send_message,
        icon_color=DEFAULT_COLOR
    )
    
    preloader = ft.ProgressRing(visible=False)
    
    page.pubsub.subscribe(on_recieve_message)


    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        preloader
    )
    
    page.add(
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
    )

ft.app(target=main)