import flet as ft


class ChatList(ft.ListView):
    def __init__(self, controls: list[ft.Control] = []):
        super().__init__()
        self.expand = True
        self.auto_scroll = True
        self.spacing = 8
        self.controls = controls
