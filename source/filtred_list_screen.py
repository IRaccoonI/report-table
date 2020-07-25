from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
from kivy.app import App

from common import set_screen
import ast

class FiltredListScreen(Screen):
    def __init__(self, **kw):
        super(FiltredListScreen, self).__init__(**kw)

    def on_enter(self):  # Будет вызвана в момент открытия экрана

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Назад в главное меню',
                             on_press=lambda x: set_screen('main'),
                             size_hint_y=None, height=dp(40))
        self.layout.add_widget(back_button)
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)


        # for f, d in sorted(dic_foods.items(), key=lambda x: x[1]):
        #     fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
        #     btn = Button(text=fd, size_hint_y=None, height=dp(40))
        #     self.layout.add_widget(btn)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.layout.clear_widgets()  # очищаем список
