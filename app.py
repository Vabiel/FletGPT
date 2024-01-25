import flet as ft
from chat_view import ChatView
from di import DI
from settings_dialog import SettingDialog
from sidebar import Sidebar


DEFAULT_COLOR = ft.colors.BLUE
DEFAULT_RADIUS = 8
DEFAULT_BORDER = ft.border.all(1, DEFAULT_COLOR)


def main(page: ft.Page):
    page.title = "FletGPT"
    di = DI.get_instance()
    di.set_storage(page.client_storage)
    dialog = SettingDialog(page)

    page.add(
        ft.Row(
            [
                Sidebar(
                    border=DEFAULT_BORDER,
                    radius=DEFAULT_RADIUS,
                    bgcolor=DEFAULT_COLOR,
                    on_settings=dialog.show,
                ),
                ChatView(DEFAULT_BORDER, DEFAULT_RADIUS, DEFAULT_COLOR),
            ],
            expand=True,
        ),
    )


ft.app(target=main)
