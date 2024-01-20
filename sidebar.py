import flet as ft


class Sidebar(ft.Container):
    def __init__(self, border, bgcolor, radius, on_settings):
        super().__init__()

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Chats history"),
                    ]
                ),
                ft.Divider(color=bgcolor, height=1),
                ft.ListView(expand=True, auto_scroll=True, spacing=8),
                ft.Divider(color=bgcolor, height=1),
                ft.TextButton("Settings", icon=ft.icons.SETTINGS, on_click=on_settings),
            ],
            expand=True,
        )
        self.padding = ft.padding.all(15)
        self.margin = ft.margin.all(0)
        self.width = 250
        self.border = border
        self.border_radius = radius
