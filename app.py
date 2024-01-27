import flet as ft
from src.controls.chat.chat_view import ChatView
from src.app.di import DI
from src.dialogs.settings_dialog import SettingDialog
from src.controls.history.history_list import HistoryList


DEFAULT_COLOR = ft.colors.BLUE
DEFAULT_RADIUS = 8
DEFAULT_BORDER = ft.border.all(1, DEFAULT_COLOR)


def main(page: ft.Page):
    page.title = "FletGPT"
    di = DI.get_instance()
    di.set_storage(page.client_storage)
    dialog = SettingDialog(page, DEFAULT_RADIUS, DEFAULT_COLOR)

    page.add(
        ft.Row(
            [
                HistoryList(
                    border=DEFAULT_BORDER,
                    radius=DEFAULT_RADIUS,
                    bgcolor=DEFAULT_COLOR,
                    on_settings=dialog.on_show,
                ),
                ChatView(DEFAULT_BORDER, DEFAULT_RADIUS, DEFAULT_COLOR),
            ],
            expand=True,
        ),
    )


ft.app(target=main)
