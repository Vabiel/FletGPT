import flet as ft


class SettingDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Settings"),
            content=ft.Column(
                [
                    ft.Dropdown(
                        label="Default GPT",
                        hint_text="Choose default provider",
                        options=[
                            ft.dropdown.Option("3.5 turbo"),
                            ft.dropdown.Option("4"),
                            ft.dropdown.Option("4 turbo"),
                        ],
                        autofocus=True,
                    )
                ],
                auto_scroll=True,
                width=400,
                height=400,
            ),
            actions=[
                ft.TextButton("Save", on_click=self.close),
                ft.TextButton("Cancel", on_click=self.close),
            ],
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def close(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def show(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()
