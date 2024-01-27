import flet as ft
from src.app.events import Event
from src.app.user_settings import UserSettings
from src.app.di import DI

from src.app.gpt_model import GPTModel


class SettingDialog:
    def __init__(self, page: ft.Page, radius, color):
        self.page = page
        self.model_selector = ft.Dropdown(
            label="Default GPT",
            hint_text="Choose default model",
            options=[ft.dropdown.Option(model) for model in GPTModel.all],
            autofocus=True,
            border_color=color,
            border_radius=radius,
        )
        self.context_depth_field = ft.TextField(
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
            label="Context depth", 
            hint_text="Enter context depth here",
            max_length=2,
            border_color=color,
            border_radius=radius,
            
        )
        self.switch = ft.Switch(label="Ignore context depth", value=False, on_change=self.__validate)
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Settings"),
            content=ft.Column(
                [
                    self.model_selector,
                    ft.Container(height=8),
                    self.switch,
                    ft.Container(height=8),
                    self.context_depth_field,
                ],
                auto_scroll=True,
                width=400,
                height=230,
            ),
            actions=[
                ft.TextButton("Save", on_click=self.__on_save),
                ft.TextButton("Cancel", on_click=self.__close),
            ],
        )
        
    def on_show(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.__load_settings()
        self.__on_ignore_change()
        self.page.update()

    def __close(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def __on_save(self, e):
        storage = self.page.client_storage
        di = DI.get_instance()
        raw_depth = self.context_depth_field.value
        model = self.model_selector.value
        ignore_value = self.switch.value
        context_depth = 40 if raw_depth == "" else raw_depth
        storage.set(UserSettings.CURRENT_MODEL, model)
        storage.set(UserSettings.IGNORE_CONTEXT_DEPTH, ignore_value)
        storage.set(UserSettings.CONTEXT_DEPTH, context_depth)
        di.eventDispatcher.dispatch(Event.ON_CHANGE_SETTINGS, (model, ignore_value, context_depth))
        self.__close(e)

    def __load_settings(self):
        storage = self.page.client_storage
        if storage.contains_key(UserSettings.CURRENT_MODEL):
            self.model_selector.value = storage.get(UserSettings.CURRENT_MODEL)
        else:
            self.model_selector.value = GPTModel.GPT_4
            storage.set(UserSettings.CURRENT_MODEL, GPTModel.GPT_4)

        if storage.contains_key(UserSettings.IGNORE_CONTEXT_DEPTH):
            self.switch.value = storage.get(UserSettings.IGNORE_CONTEXT_DEPTH)
        else:
            self.switch.value = False
            storage.set(UserSettings.IGNORE_CONTEXT_DEPTH, False)
            
        if storage.contains_key(UserSettings.CONTEXT_DEPTH):
            self.context_depth_field.value = storage.get(UserSettings.CONTEXT_DEPTH)
        else:
            self.context_depth_field.value = 40
            storage.set(UserSettings.CONTEXT_DEPTH, 40)
            
    def __on_ignore_change(self):
        self.context_depth_field.read_only = self.switch.value
        self.context_depth_field.opacity = 0.5 if self.switch.value else 1
        
        
    def __validate(self, e):
        self.__on_ignore_change()
        self.context_depth_field.update()
