import flet as ft
from src.controls.chat.chat_view import ChatView
from src.app.di import DI
from src.controls.history.history_list import HistoryList


DEFAULT_COLOR = ft.colors.BLUE
DEFAULT_RADIUS = 8
DEFAULT_BORDER = ft.border.all(1, DEFAULT_COLOR)


def main(page: ft.Page):
    page.title = "FletGPT"
    di = DI.get_instance()
    di.set_storage(page.client_storage)

    page.add(
        ft.Row(
            [
                HistoryList(
                    page,
                    border=DEFAULT_BORDER,
                    radius=DEFAULT_RADIUS,
                    bgcolor=DEFAULT_COLOR,
                ),
                ChatView(DEFAULT_BORDER, DEFAULT_RADIUS, DEFAULT_COLOR),
            ],
            expand=True,
        ),
    )


ft.app(target=main)
